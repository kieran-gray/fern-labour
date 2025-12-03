use anyhow::{Result, anyhow};
use std::collections::HashMap;
use worker::Headers;

use super::WebhookVerifier;

pub struct WebhookVerificationService {
    verifiers: HashMap<String, Box<dyn WebhookVerifier>>,
}

impl WebhookVerificationService {
    pub fn create(verifiers: Vec<Box<dyn WebhookVerifier>>) -> Self {
        let verifier_map: HashMap<String, Box<dyn WebhookVerifier>> = verifiers
            .into_iter()
            .map(|verifier| (verifier.provider_name().to_string(), verifier))
            .collect();

        Self {
            verifiers: verifier_map,
        }
    }

    pub fn verify(&self, provider: &str, headers: &Headers, body: &[u8]) -> Result<()> {
        let verifier = self
            .verifiers
            .get(provider)
            .ok_or_else(|| anyhow!("No verifier configured for provider: {}", provider))?;

        verifier.verify(headers, body)
    }
}
