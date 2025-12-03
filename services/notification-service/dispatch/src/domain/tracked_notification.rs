use chrono::{DateTime, Utc};
use fern_labour_notifications_shared::value_objects::NotificationChannel;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrackedNotification {
    pub external_id: String,
    pub notification_id: Uuid,
    pub channel: NotificationChannel,
    pub provider: String,
    pub created_at: DateTime<Utc>,
}
