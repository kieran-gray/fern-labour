use anyhow::{Context, Result};
use chrono::{DateTime, Utc};
use fern_labour_notifications_shared::value_objects::NotificationChannel;
use serde::{Deserialize, Serialize};
use std::str::FromStr;
use uuid::Uuid;

use crate::domain::tracked_notification::TrackedNotification;

#[derive(Debug, Serialize, Deserialize)]
pub struct TrackedNotificationRow {
    pub external_id: String,
    pub notification_id: String,
    pub channel: String,
    pub provider: String,
    pub created_at: String,
}

impl TrackedNotificationRow {
    pub fn from_tracked_notification(tracked_notification: &TrackedNotification) -> Result<Self> {
        Ok(Self {
            notification_id: tracked_notification.notification_id.to_string(),
            external_id: tracked_notification.external_id.to_string(),
            channel: tracked_notification.channel.to_string(),
            provider: tracked_notification.provider.to_string(),
            created_at: tracked_notification.created_at.to_string(),
        })
    }

    pub fn to_tracked_notification(&self) -> Result<TrackedNotification> {
        let notification_id = Uuid::parse_str(&self.notification_id)
            .context(format!("Invalid UUID: {}", self.notification_id))?;

        let channel = NotificationChannel::from_str(&self.channel)
            .context(format!("Invalid channel: {}", self.channel))?;

        let created_at: DateTime<Utc> = self
            .created_at
            .parse()
            .context(format!("Invalid create_at: {}", self.created_at))?;

        Ok(TrackedNotification {
            external_id: self.external_id.clone(),
            notification_id,
            channel,
            provider: self.provider.clone(),
            created_at,
        })
    }
}
