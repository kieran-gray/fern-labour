use crate::application::{
    dtos::notification_content::NotificationContentDTO, exceptions::AppError,
};

use async_trait::async_trait;

#[async_trait]
pub trait NotificationGenerationServiceTrait: Send + Sync {
    async fn generate_content(
        &self,
        notification_id: &str,
    ) -> Result<NotificationContentDTO, AppError>;
}
