use std::collections::HashMap;

use async_trait::async_trait;

use crate::{
    service_clients::notification::exceptions::NotificationClientError,
    value_objects::{NotificationChannel, NotificationPriority, NotificationTemplateData},
};

#[async_trait(?Send)]
pub trait NotificationClient {
    async fn request_notification(
        &self,
        channel: NotificationChannel,
        destination: String,
        template_data: NotificationTemplateData,
        metadata: Option<HashMap<String, String>>,
        priority: NotificationPriority,
    ) -> Result<(), NotificationClientError>;
}
