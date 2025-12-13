use anyhow::Result;
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::{AsyncRepositoryTrait, DecodedCursor};

use crate::read_models::notification_status::read_model::NotificationStatus;

#[async_trait(?Send)]
pub trait NotificationStatusQueryHandler {
    async fn get_notifications(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<NotificationStatus>>;
}

pub struct NotificationStatusQuery {
    repository: Box<dyn AsyncRepositoryTrait<NotificationStatus>>,
}

impl NotificationStatusQuery {
    pub fn create(repository: Box<dyn AsyncRepositoryTrait<NotificationStatus>>) -> Self {
        Self { repository }
    }
}

#[async_trait(?Send)]
impl NotificationStatusQueryHandler for NotificationStatusQuery {
    async fn get_notifications(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<NotificationStatus>> {
        let notifications = self.repository.get(limit, cursor).await?;

        Ok(notifications)
    }
}
