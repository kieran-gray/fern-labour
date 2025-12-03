use std::sync::Arc;

use crate::domain::{
    entity::ContactMessage, exceptions::RepositoryError,
    repository::ContactMessageRepository as ContactMessageRepositoryInterface,
};
use crate::infrastructure::persistence::models::{ActivityRow, ContactMessageRow};
use async_trait::async_trait;
use chrono::{DateTime, Duration, NaiveDate, Utc};
use worker::D1Database;

pub struct ContactMessageRepository {
    db: D1Database,
}

impl ContactMessageRepository {
    pub fn create(db: D1Database) -> Arc<dyn ContactMessageRepositoryInterface> {
        Arc::new(Self { db })
    }
}

#[async_trait(?Send)]
impl ContactMessageRepositoryInterface for ContactMessageRepository {
    async fn save(&self, contact: &ContactMessage) -> Result<bool, RepositoryError> {
        let row = ContactMessageRow::from_contact_message(contact)?;

        let statement = self.db.prepare(
            "INSERT INTO contact_messages (id, category, email, name, message, data, received_at)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
        );

        let result = statement
            .bind(&[
                row.id.into(),
                row.category.into(),
                row.email.into(),
                row.name.into(),
                row.message.into(),
                row.data.into(),
                row.received_at.into(),
            ])
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to bind parameters: {e}")))?
            .run()
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to execute query: {e}")))?;

        Ok(result.success())
    }

    async fn get(&self) -> Result<Vec<ContactMessage>, RepositoryError> {
        let statement = self.db.prepare(
            "SELECT id, category, email, name, message, data, received_at FROM contact_messages ORDER BY received_at DESC",
        );

        let result = statement
            .all()
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to execute query: {e}")))?;

        let rows: Vec<ContactMessageRow> = result.results().map_err(|e| {
            RepositoryError::DatabaseError(format!("Failed to deserialize rows: {e}"))
        })?;

        rows.into_iter()
            .map(|row| row.to_contact_message())
            .collect()
    }

    async fn get_paginated(
        &self,
        limit: i64,
        offset: i64,
    ) -> Result<Vec<ContactMessage>, RepositoryError> {
        let statement = self.db.prepare(
            "SELECT id, category, email, name, message, data, received_at FROM contact_messages ORDER BY received_at DESC LIMIT ?1 OFFSET ?2",
        ).bind(&[(limit as f64).into(), (offset as f64).into()])
        .map_err(|e| RepositoryError::DatabaseError(format!("Failed to bind parameters: {e}")))?;

        let result = statement
            .all()
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to execute query: {e}")))?;

        let rows: Vec<ContactMessageRow> = result.results().map_err(|e| {
            RepositoryError::DatabaseError(format!("Failed to deserialize rows: {e}"))
        })?;

        rows.into_iter()
            .map(|row| row.to_contact_message())
            .collect()
    }

    async fn get_activity(&self, days: i64) -> Result<Vec<(i64, DateTime<Utc>)>, RepositoryError> {
        let days_ago = Utc::now() - Duration::days(days);
        let threshold = days_ago.to_rfc3339();

        let statement = self
            .db
            .prepare(
                "SELECT COUNT(*) as row_count, substr(received_at, 1, 10) as date
             FROM contact_messages
             WHERE received_at >= ?1 AND received_at IS NOT NULL
             GROUP BY substr(received_at, 1, 10)
             ORDER BY date",
            )
            .bind(&[threshold.into()])
            .map_err(|err| {
                RepositoryError::DatabaseError(format!("Failed to bind params: {err}"))
            })?;

        let result = statement
            .all()
            .await
            .map_err(|e| RepositoryError::DatabaseError(format!("Failed to execute query: {e}")))?;

        let rows: Vec<ActivityRow> = result.results().map_err(|e| {
            RepositoryError::DatabaseError(format!("Failed to deserialize rows: {e}"))
        })?;

        rows.into_iter()
            .map(|row| {
                let naive_date = NaiveDate::parse_from_str(&row.date, "%Y-%m-%d").map_err(|e| {
                    RepositoryError::DatabaseError(format!("Invalid date format: {e}"))
                })?;

                let datetime = naive_date
                    .and_hms_opt(0, 0, 0)
                    .ok_or_else(|| {
                        RepositoryError::DatabaseError("Failed to create datetime".to_string())
                    })?
                    .and_utc();

                Ok((row.row_count, datetime))
            })
            .collect()
    }
}
