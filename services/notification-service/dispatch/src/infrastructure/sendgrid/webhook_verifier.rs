use anyhow::{Context, Result, anyhow};
use base64::{Engine, engine::general_purpose::STANDARD};
use hmac::{Hmac, Mac};
use sha2::Sha256;
use worker::Headers;

use crate::application::webhook::WebhookVerifier;

/// Reference: https://docs.sendgrid.com/for-developers/tracking-events/getting-started-event-webhook-security-features
pub struct SendgridWebhookVerifier {
    verification_key: String,
}

impl SendgridWebhookVerifier {
    pub fn create(verification_key: String) -> Self {
        Self { verification_key }
    }
}

impl WebhookVerifier for SendgridWebhookVerifier {
    fn provider_name(&self) -> &str {
        "sendgrid"
    }

    fn verify(&self, headers: &Headers, body: &[u8]) -> Result<()> {
        let signature = headers
            .get("X-Twilio-Email-Event-Webhook-Signature")
            .context("Failed to read webhook signature header")?
            .ok_or_else(|| anyhow!("Missing X-Twilio-Email-Event-Webhook-Signature header"))?;

        let timestamp = headers
            .get("X-Twilio-Email-Event-Webhook-Timestamp")
            .context("Failed to read webhook timestamp header")?
            .ok_or_else(|| anyhow!("Missing X-Twilio-Email-Event-Webhook-Timestamp header"))?;

        let payload = format!("{}{}", timestamp, String::from_utf8_lossy(body));

        let mut mac = Hmac::<Sha256>::new_from_slice(self.verification_key.as_bytes())
            .map_err(|e| anyhow!("Invalid verification key: {}", e))?;
        mac.update(payload.as_bytes());

        let result = mac.finalize();
        let expected_signature = STANDARD.encode(result.into_bytes());

        if signature != expected_signature {
            return Err(anyhow!("Webhook signature verification failed"));
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_verifier_creation() {
        let verifier = SendgridWebhookVerifier::create("test-key".to_string());
        assert_eq!(verifier.provider_name(), "sendgrid");
    }
}
