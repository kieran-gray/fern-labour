use serde::{Deserialize, Serialize};

/// Reference: https://resend.com/docs/dashboard/webhooks/event-types
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResendWebhookEvent {
    #[serde(rename = "type")]
    pub event_type: String,
    pub created_at: String,
    pub data: ResendEventData,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResendEventData {
    pub email_id: String,
    pub to: Vec<String>,
    pub from: String,
    pub subject: String,
}

impl ResendWebhookEvent {
    pub fn external_id(&self) -> String {
        self.data.email_id.clone()
    }

    pub fn event_type(&self) -> &str {
        &self.event_type
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_deserialize_resend_webhook() {
        let json = r#"{
            "type": "email.delivered",
            "created_at": "2024-01-01T12:00:00Z",
            "data": {
                "email_id": "re_abc123",
                "to": ["test@example.com"],
                "from": "sender@example.com",
                "subject": "Test Email"
            }
        }"#;

        let event: ResendWebhookEvent = serde_json::from_str(json).unwrap();
        assert_eq!(event.event_type, "email.delivered");
        assert_eq!(event.external_id(), "re_abc123");
    }
}
