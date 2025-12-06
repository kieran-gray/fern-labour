use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct DispatchResponse {
    pub external_id: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct WebhookInterpretationResponse {
    pub notification_id: String,
    pub status: String,
}
