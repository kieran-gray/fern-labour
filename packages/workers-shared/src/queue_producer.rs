use anyhow::{Context, Result};
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::{QueueMessage, QueueProducerTrait};
use serde::Serialize;
use tracing::debug;
use worker::Queue;

pub struct NotificationQueueProducer {
    queue: Queue,
}

impl NotificationQueueProducer {
    pub fn create(
        queue: Queue,
    ) -> Box<dyn QueueProducerTrait<Envelope = CommandEnvelope<QueueMessage>>> {
        Box::new(Self { queue })
    }

    fn serialize_envelope<T: Serialize>(&self, envelope: &T) -> Result<String> {
        serde_json::to_string(envelope).context("Failed to serialize envelope for queue")
    }
}

#[async_trait(?Send)]
impl QueueProducerTrait for NotificationQueueProducer {
    type Envelope = CommandEnvelope<QueueMessage>;

    async fn publish(&self, envelope: Self::Envelope) -> Result<()> {
        debug!(
            command = envelope.command.command_name(),
            aggregate_id = %envelope.metadata.aggregate_id,
            correlation_id = %envelope.metadata.correlation_id,
            "Publishing command envelope to queue"
        );

        let json_string = self.serialize(&envelope)?;

        self.queue
            .send(&json_string)
            .await
            .map_err(|e| anyhow::anyhow!("Failed to send message to queue: {}", e))?;

        Ok(())
    }

    async fn publish_batch(&self, envelope_batch: Vec<Self::Envelope>) -> Result<()> {
        let json_messages: Result<Vec<String>> = envelope_batch
            .iter()
            .map(|envelope| self.serialize(envelope))
            .collect();

        self.queue
            .send_batch(json_messages?)
            .await
            .context("Failed to publish envelope batch to queue")?;

        Ok(())
    }

    fn serialize(&self, envelope: &Self::Envelope) -> Result<String> {
        self.serialize_envelope(envelope)
    }
}
