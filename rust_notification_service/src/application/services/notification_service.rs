use std::collections::HashMap;

use crate::application::{dtos::notification::NotificationDTO, exceptions::AppError};

use async_trait::async_trait;

#[async_trait]
pub trait NotificationServiceTrait: Send + Sync {
    async fn create_notification(
        &self,
        channel: String,
        destination: String,
        template: String,
        data: HashMap<String, String>,
        metadata: Option<HashMap<String, String>>,
        status: Option<String>,
    ) -> Result<NotificationDTO, AppError>;

    async fn update_notification(
        &self,
        notification_id: String,
        status: String,
        external_id: Option<String>,
    ) -> Result<NotificationDTO, AppError>;

    async fn status_callback(&self, external_id: String, status: String) -> Result<bool, AppError>;
}
