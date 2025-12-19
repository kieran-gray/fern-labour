use anyhow::{Context, Result, anyhow};
use fern_labour_workers_shared::clients::worker_clients::auth::User;
use serde::{Deserialize, Serialize};
use worker::SqlStorage;

pub struct UserStorage {
    sql: SqlStorage,
}

#[derive(Debug, Serialize, Deserialize)]
struct UserRow {
    user_id: String,
    issuer: String,
    email: Option<String>,
    phone_number: Option<String>,
    first_name: Option<String>,
    last_name: Option<String>,
    name: Option<String>,
}

impl From<UserRow> for User {
    fn from(row: UserRow) -> Self {
        User {
            user_id: row.user_id,
            issuer: row.issuer,
            email: row.email,
            phone_number: row.phone_number,
            first_name: row.first_name,
            last_name: row.last_name,
            name: row.name,
        }
    }
}

impl UserStorage {
    pub fn create(sql: SqlStorage) -> Self {
        Self { sql }
    }

    pub fn init_schema(&self) -> Result<()> {
        self.sql
            .exec(
                "CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    issuer TEXT NOT NULL,
                    email TEXT,
                    phone_number TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    name TEXT
                )",
                None,
            )
            .map_err(|err| anyhow!("Failed to create users table: {err}"))?;

        Ok(())
    }

    pub fn get(&self) -> Result<Vec<User>> {
        let result = self
            .sql
            .exec("SELECT * FROM users", None)?
            .to_array::<UserRow>()?
            .into_iter()
            .map(|r| r.into())
            .collect();
        Ok(result)
    }

    pub fn get_user(&self, user_id: &str) -> Result<Vec<User>> {
        let result = self
            .sql
            .exec(
                "SELECT * FROM users WHERE user_id = ?1",
                Some(vec![user_id.into()]),
            )?
            .to_array::<UserRow>()?
            .into_iter()
            .map(|r| r.into())
            .collect();
        Ok(result)
    }

    pub fn save_user(&self, user: &User) -> Result<()> {
        self.sql
            .exec(
                "INSERT OR REPLACE INTO users (user_id, issuer, email, phone_number, first_name, last_name, name)
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
                Some(vec![
                    user.user_id.clone().into(),
                    user.issuer.clone().into(),
                    user.email.clone().into(),
                    user.phone_number.clone().into(),
                    user.first_name.clone().into(),
                    user.last_name.clone().into(),
                    user.name.clone().into(),
                ]),
            )
            .context("Failed to save user to storage")?;
        Ok(())
    }

    pub fn save_user_if_not_exists(&self, user: &User) -> Result<bool> {
        let existing = self.get_user(&user.user_id)?;

        if existing.is_empty() {
            self.save_user(user)?;
            Ok(true)
        } else {
            Ok(false)
        }
    }
}
