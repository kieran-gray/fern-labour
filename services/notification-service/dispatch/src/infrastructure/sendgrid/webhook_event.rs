use serde::{Deserialize, Serialize};

/// Reference: https://docs.sendgrid.com/for-developers/tracking-events/event
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SendgridWebhookEvent {
    pub event: String,
    pub email: String,
    pub timestamp: i64,
    pub sg_message_id: Option<String>,
}

impl SendgridWebhookEvent {
    pub fn external_id(&self) -> Option<String> {
        self.sg_message_id.clone()
    }

    pub fn event_type(&self) -> &str {
        &self.event
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_deserialize_sendgrid_webhook() {
        let json = r#"{
            "email": "test@example.com",
            "timestamp": 1699876543,
            "sg_message_id": "msg_abc123",
            "event": "delivered",
            "custom_args": {}
        }"#;

        let event: SendgridWebhookEvent = serde_json::from_str(json).unwrap();
        assert_eq!(event.event, "delivered");
        assert_eq!(event.email, "test@example.com");
        assert_eq!(event.external_id().unwrap(), "msg_abc123");
    }
}
