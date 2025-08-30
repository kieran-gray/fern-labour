use std::collections::HashMap;

use crate::domain::entity::Notification;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NotificationDTO {
    pub id: String,
    pub status: String,
    pub channel: String,
    pub destination: String,
    pub template: String,
    pub data: HashMap<String, String>,
    pub metadata: Option<HashMap<String, String>>,
    pub external_id: Option<String>,
}

impl From<Notification> for NotificationDTO {
    fn from(notification: Notification) -> Self {
        Self {
            id: notification.id.to_string(),
            status: notification.status.to_string(),
            channel: notification.channel.to_string(),
            destination: notification.destination,
            template: notification.template.to_string(),
            data: notification.data,
            metadata: notification.metadata,
            external_id: notification.external_id,
        }
    }
}
