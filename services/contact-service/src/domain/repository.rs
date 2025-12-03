use super::entity::ContactMessage;
use super::exceptions::RepositoryError;

use async_trait::async_trait;
use chrono::{DateTime, Utc};

#[async_trait(?Send)]
/// Trait representing repository-level operations for Contact Message entities.
/// Provides methods for saving, retrieving, updating, and deleting Contact Messages in the database.
pub trait ContactMessageRepository: Send + Sync {
    async fn save(&self, contact: &ContactMessage) -> Result<bool, RepositoryError>;
    async fn get(&self) -> Result<Vec<ContactMessage>, RepositoryError>;
    async fn get_paginated(
        &self,
        limit: i64,
        offset: i64,
    ) -> Result<Vec<ContactMessage>, RepositoryError>;
    async fn get_activity(&self, days: i64) -> Result<Vec<(i64, DateTime<Utc>)>, RepositoryError>;
}
