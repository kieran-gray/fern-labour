use super::entity::Notification;

use async_trait::async_trait;
use sqlx::{Postgres, Pool, Transaction};

#[async_trait]
/// Trait representing repository-level operations for Notification entities.
/// Provides methods for saving, retrieving, updating, and deleting Notifications in the database.
pub trait NotificationRepository: Send + Sync {
    async fn find_all(&self, pool: Pool<Postgres>) -> Result<Vec<Notification>, sqlx::Error>;

    async fn get_by_id(&self, pool: Pool<Postgres>, id: String) -> Result<Option<Notification>, sqlx::Error>;

    async fn get_by_external_id(&self, pool: Pool<Postgres>, external_id: String) -> Result<Option<Notification>, sqlx::Error>;

    async fn save(
        &self,
        tx: &mut Transaction<'_, Postgres>,
        notification: Notification,
    ) -> Result<String, sqlx::Error>;

    async fn update(
        &self,
        tx: &mut Transaction<'_, Postgres>,
        notification: Notification,
    ) -> Result<Option<Notification>, sqlx::Error>;

    async fn delete(
        &self,
        tx: &mut Transaction<'_, Postgres>,
        notification: Notification,
    ) -> Result<bool, sqlx::Error>;
}