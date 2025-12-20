use std::collections::HashMap;

use serde::{Deserialize, Serialize};

use crate::value_objects::{NotificationPriority, NotificationTemplateData};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NotificationRequest {
    pub channel: String,
    pub destination: String,
    pub template_data: NotificationTemplateData,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub metadata: Option<HashMap<String, String>>,
    #[serde(default)]
    pub priority: NotificationPriority,
}
