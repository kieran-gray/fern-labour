use anyhow::{Context, Result};
use async_trait::async_trait;
use serde::Serialize;

#[async_trait(?Send)]
pub trait QueueProducerTrait: Send + Sync {
    type Envelope: Serialize;

    fn serialize(&self, message: &Self::Envelope) -> Result<String> {
        serde_json::to_string(message).context("Failed to serialize integration event")
    }

    fn serialize_batch(&self, message_batch: &[Self::Envelope]) -> Result<Vec<String>> {
        message_batch
            .iter()
            .map(|message| self.serialize(message))
            .collect::<Result<Vec<_>, _>>()
            .context("Failed to serialize integration event batch")
    }

    async fn publish(&self, message: Self::Envelope) -> Result<()>;
    async fn publish_batch(&self, message_batch: Vec<Self::Envelope>) -> Result<()>;
}
