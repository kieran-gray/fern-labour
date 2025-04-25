use super::entity::Notification;

use async_trait::async_trait;
use uuid::Uuid;

#[async_trait]
/// Trait representing repository-level operations for Notification entities.
/// Provides methods for saving, retrieving, updating, and deleting Notifications in the database.
pub trait NotificationRepository: Send + Sync {
    async fn get_by_id(&self, id: Uuid) -> Result<Option<Notification>, sqlx::Error>;

    async fn get_by_external_id(
        &self,
        external_id: String,
    ) -> Result<Option<Notification>, sqlx::Error>;

    async fn save(&self, notification: &Notification) -> Result<bool, sqlx::Error>;

    async fn delete(&self, notification: &Notification) -> Result<bool, sqlx::Error>;
}
