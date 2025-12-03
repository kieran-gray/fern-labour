use anyhow::Result;
use async_trait::async_trait;

use crate::read_models::notification_activity::{
    read_model::NotificationActivity, repository::NotificationActivityRepository,
};

#[async_trait(?Send)]
pub trait NotificationActivityQueryHandler {
    async fn get_activity_for_days(
        &self,
        number_of_days: usize,
    ) -> Result<Vec<NotificationActivity>>;
}

pub struct NotificationActivityQuery {
    repository: Box<dyn NotificationActivityRepository>,
}

impl NotificationActivityQuery {
    pub fn create(repository: Box<dyn NotificationActivityRepository>) -> Self {
        Self { repository }
    }
}

#[async_trait(?Send)]
impl NotificationActivityQueryHandler for NotificationActivityQuery {
    async fn get_activity_for_days(
        &self,
        number_of_days: usize,
    ) -> Result<Vec<NotificationActivity>> {
        let notifications = self.repository.get(number_of_days).await?;

        Ok(notifications)
    }
}
