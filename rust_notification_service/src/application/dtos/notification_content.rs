use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct NotificationContentDTO {
    pub message: String,
    pub subject: Option<String>,
}
