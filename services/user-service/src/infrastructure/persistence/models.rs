use crate::domain::{
    entity::User,
    exceptions::RepositoryError,
    value_objects::{Email, PhoneNumber, UserId},
};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct UserRow {
    pub id: String,
    pub email: String,
    pub first_name: String,
    pub last_name: String,
    pub phone_number: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl UserRow {
    pub fn from_user(user: &User) -> Result<Self, RepositoryError> {
        Ok(Self {
            id: user.id.value().to_string(),
            email: user.email.value().to_string(),
            first_name: user.first_name.clone(),
            last_name: user.last_name.clone(),
            phone_number: user.phone_number.as_ref().map(|p| p.value().to_string()),
            created_at: user.created_at.to_rfc3339(),
            updated_at: user.updated_at.to_rfc3339(),
        })
    }

    pub fn to_user(&self) -> Result<User, RepositoryError> {
        let id = UserId::new(self.id.clone())
            .map_err(|e| RepositoryError::DatabaseError(format!("Invalid user ID: {e}")))?;

        let email = Email::new(self.email.clone())
            .map_err(|e| RepositoryError::DatabaseError(format!("Invalid email: {e}")))?;

        let phone_number = match &self.phone_number {
            Some(phone) if !phone.is_empty() => {
                Some(PhoneNumber::new(phone.clone()).map_err(|e| {
                    RepositoryError::DatabaseError(format!("Invalid phone number: {e}"))
                })?)
            }
            _ => None,
        };

        let created_at: DateTime<Utc> = self.created_at.parse().map_err(|e| {
            RepositoryError::DatabaseError(format!("Failed to parse created_at: {e}"))
        })?;

        let updated_at: DateTime<Utc> = self.updated_at.parse().map_err(|e| {
            RepositoryError::DatabaseError(format!("Failed to parse updated_at: {e}"))
        })?;

        Ok(User {
            id,
            email,
            first_name: self.first_name.clone(),
            last_name: self.last_name.clone(),
            phone_number,
            created_at,
            updated_at,
        })
    }
}
