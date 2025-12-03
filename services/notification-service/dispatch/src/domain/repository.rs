use anyhow::Result;
use async_trait::async_trait;

use crate::domain::tracked_notification::TrackedNotification;

#[async_trait(?Send)]
pub trait TrackedNotificationRepositoryTrait: Send + Sync {
    async fn get(&self, external_id: &str) -> Result<TrackedNotification>;
    async fn put(&self, tracked_notification: &TrackedNotification) -> Result<()>;
}
