use std::sync::Arc;

use crate::domain::{
    entity::User, exceptions::RepositoryError,
    repository::UserRepository as UserRepositoryInterface, value_objects::UserId,
};
use crate::infrastructure::persistence::models::UserRow;
use async_trait::async_trait;
use worker::D1Database;

pub struct UserRepository {
    db: D1Database,
}

impl UserRepository {
    pub fn create(db: D1Database) -> Arc<dyn UserRepositoryInterface> {
        Arc::new(Self { db })
    }
}

#[async_trait(?Send)]
impl UserRepositoryInterface for UserRepository {
    async fn save(&self, user: &User) -> Result<(), RepositoryError> {
        let row = UserRow::from_user(user)?;

        let statement = self.db.prepare(
            "INSERT OR REPLACE INTO users (id, email, first_name, last_name, phone_number, created_at, updated_at)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
        );

        statement
            .bind(&[
                row.id.into(),
                row.email.into(),
                row.first_name.into(),
                row.last_name.into(),
                row.phone_number
                    .map(|p| p.into())
                    .unwrap_or_else(|| worker::wasm_bindgen::JsValue::NULL),
                row.created_at.into(),
                row.updated_at.into(),
            ])
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to bind parameters: {e}")))?
            .run()
            .await
            .map_err(|e| RepositoryError::SaveFailed(format!("Failed to save user: {e}")))?;

        Ok(())
    }

    async fn get_by_id(&self, user_id: &UserId) -> Result<Option<User>, RepositoryError> {
        let statement = self.db.prepare(
            "SELECT id, email, first_name, last_name, phone_number, created_at, updated_at
             FROM users
             WHERE id = ?1",
        );

        let result = statement
            .bind(&[user_id.value().into()])
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to bind parameters: {e}")))?
            .first::<UserRow>(None)
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to execute query: {e}")))?;

        match result {
            Some(row) => Ok(Some(row.to_user()?)),
            None => Ok(None),
        }
    }

    async fn get_by_email(&self, email: &str) -> Result<Option<User>, RepositoryError> {
        let statement = self.db.prepare(
            "SELECT id, email, first_name, last_name, phone_number, created_at, updated_at
             FROM users
             WHERE email = ?1",
        );

        let result = statement
            .bind(&[email.into()])
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to bind parameters: {e}")))?
            .first::<UserRow>(None)
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to execute query: {e}")))?;

        match result {
            Some(row) => Ok(Some(row.to_user()?)),
            None => Ok(None),
        }
    }

    async fn exists(&self, user_id: &UserId) -> Result<bool, RepositoryError> {
        let statement = self
            .db
            .prepare("SELECT COUNT(*) as count FROM users WHERE id = ?1");

        #[derive(serde::Deserialize)]
        struct CountRow {
            count: i64,
        }

        let result = statement
            .bind(&[user_id.value().into()])
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to bind parameters: {e}")))?
            .first::<CountRow>(None)
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to execute query: {e}")))?;

        Ok(result.map(|r| r.count > 0).unwrap_or(false))
    }

    async fn delete(&self, user_id: &UserId) -> Result<(), RepositoryError> {
        let statement = self.db.prepare("DELETE FROM users WHERE id = ?1");

        statement
            .bind(&[user_id.value().into()])
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to bind parameters: {e}")))?
            .run()
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to delete user: {e}")))?;

        Ok(())
    }
}
