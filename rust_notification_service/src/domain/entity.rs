use std::collections::HashMap;

use serde::{Deserialize, Serialize};
use uuid::Uuid;

use super::enums::{NotificationStatus, NotificationTemplate, NotificationType};

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct Notification {
    pub id: Uuid,
    pub status: NotificationStatus,
    pub notification_type: NotificationType,
    pub destination: String,
    pub template: NotificationTemplate,
    pub data: HashMap<String, String>,
    pub metadata: Option<HashMap<String, String>>,
    pub external_id: Option<String>,
}

impl Notification {
    pub fn create(
        notification_type: NotificationType,
        destination: String,
        template: NotificationTemplate,
        data: HashMap<String, String>,
        status: Option<NotificationStatus>,
        metadata: Option<HashMap<String, String>>,
    ) -> Self {
        return Self {
            id: Uuid::now_v7(),
            status: status.unwrap_or(NotificationStatus::CREATED),
            notification_type,
            destination,
            template,
            data,
            metadata,
            external_id: None,
        };
    }
}
