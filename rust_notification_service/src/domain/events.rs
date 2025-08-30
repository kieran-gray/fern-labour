use std::collections::HashMap;

use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct NotificationRequestedData {
    pub channel: String,
    pub destination: String,
    pub template: String,
    pub data: HashMap<String, String>,
    pub metadata: Option<HashMap<String, String>>,
}
