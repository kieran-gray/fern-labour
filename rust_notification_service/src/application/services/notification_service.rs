use std::collections::HashMap;

use crate::application::{dtos::NotificationDTO, exceptions::AppError};

use async_trait::async_trait;

#[async_trait]
pub trait NotificationServiceTrait: Send + Sync {
    async fn create_notification(
        &self,
        notification_type: String,
        destination: String,
        template: String,
        data: HashMap<String, String>,
        metadata: Option<HashMap<String, String>>,
        status: Option<String>,
    ) -> Result<NotificationDTO, AppError>;
}