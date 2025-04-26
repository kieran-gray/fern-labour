use crate::domain::events::NotificationRequestedData;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Event {
    pub id: String,
    pub event_type: String,
    pub time: DateTime<Utc>,
    pub data: NotificationRequestedData,
}
