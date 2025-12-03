use serde::{Deserialize, Serialize};

/// Reference: https://www.twilio.com/docs/messaging/guides/track-outbound-message-status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TwilioWebhookEvent {
    #[serde(rename = "MessageSid")]
    pub message_sid: String,
    #[serde(rename = "MessageStatus")]
    pub message_status: String,
}

impl TwilioWebhookEvent {
    pub fn external_id(&self) -> String {
        self.message_sid.clone()
    }

    pub fn event_type(&self) -> &str {
        &self.message_status
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_deserialize_twilio_webhook() {
        let json = r#"{
            "MessageSid": "SM_abc123",
            "MessageStatus": "delivered",
            "To": "+15551234567",
            "From": "+15559876543"
        }"#;

        let event: TwilioWebhookEvent = serde_json::from_str(json).unwrap();
        assert_eq!(event.message_status, "delivered");
        assert_eq!(event.external_id(), "SM_abc123");
    }
}
