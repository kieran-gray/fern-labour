use anyhow::Result;
use worker::Headers;

pub trait WebhookVerifier: Send + Sync {
    fn provider_name(&self) -> &str;

    fn verify(&self, headers: &Headers, body: &[u8]) -> Result<()>;
}
