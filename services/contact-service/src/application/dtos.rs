use std::collections::HashMap;

use crate::domain::entity::ContactMessage;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContactMessageDTO {
    pub id: String,
    pub category: String,
    pub email: String,
    pub name: String,
    pub message: String,
    pub data: Option<HashMap<String, String>>,
    pub received_at: String,
}

impl From<ContactMessage> for ContactMessageDTO {
    fn from(contact_message: ContactMessage) -> Self {
        Self {
            id: contact_message.id.to_string(),
            category: contact_message.category.to_string(),
            email: contact_message.email,
            name: contact_message.name,
            message: contact_message.message,
            data: contact_message.data,
            received_at: contact_message.received_at.to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContactMessageActivityDTO {
    pub count: i64,
    pub date: DateTime<Utc>,
}

impl ContactMessageActivityDTO {
    pub fn new(count: i64, date: DateTime<Utc>) -> Self {
        Self { count, date }
    }
}

impl From<(i64, DateTime<Utc>)> for ContactMessageActivityDTO {
    fn from(value: (i64, DateTime<Utc>)) -> Self {
        Self {
            count: value.0,
            date: value.1,
        }
    }
}
