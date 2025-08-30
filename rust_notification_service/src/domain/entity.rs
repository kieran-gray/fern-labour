use std::collections::HashMap;

use serde::{Deserialize, Serialize};
use uuid::Uuid;

use super::enums::{NotificationChannel, NotificationStatus, NotificationTemplate};

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct Notification {
    pub id: Uuid,
    pub status: NotificationStatus,
    pub channel: NotificationChannel,
    pub destination: String,
    pub template: NotificationTemplate,
    pub data: HashMap<String, String>,
    pub metadata: Option<HashMap<String, String>>,
    pub external_id: Option<String>,
}

impl Notification {
    pub fn create(
        channel: NotificationChannel,
        destination: String,
        template: NotificationTemplate,
        data: HashMap<String, String>,
        status: Option<NotificationStatus>,
        metadata: Option<HashMap<String, String>>,
    ) -> Self {
        return Self {
            id: Uuid::now_v7(),
            status: status.unwrap_or(NotificationStatus::CREATED),
            channel,
            destination,
            template,
            data,
            metadata,
            external_id: None,
        };
    }

    pub fn set_external_id(&mut self, external_id: String) {
        self.external_id = Some(external_id);
    }

    pub fn set_status(&mut self, status: NotificationStatus) {
        self.status = status;
    }
}
