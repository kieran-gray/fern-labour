use anyhow::{Result, anyhow};
use async_trait::async_trait;
use fern_labour_labour_shared::value_objects::subscriber::status::SubscriberStatus;
use tracing::info;

use fern_labour_event_sourcing_rs::{AsyncProjector, AsyncRepositoryTrait, EventEnvelope};

use crate::durable_object::{
    read_side::read_models::subscription_status::SubscriptionStatusReadModel,
    write_side::domain::LabourEvent,
};

pub struct SubscriptionStatusReadModelProjector {
    name: String,
    repository: Box<dyn AsyncRepositoryTrait<SubscriptionStatusReadModel>>,
}

impl SubscriptionStatusReadModelProjector {
    pub fn create(repository: Box<dyn AsyncRepositoryTrait<SubscriptionStatusReadModel>>) -> Self {
        Self {
            name: "SubscriptionStatusReadModelProjector".to_string(),
            repository,
        }
    }

    async fn project_event(
        &self,
        model: Option<SubscriptionStatusReadModel>,
        envelope: &EventEnvelope<LabourEvent>,
    ) -> Option<SubscriptionStatusReadModel> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            LabourEvent::SubscriberRequested(e) if model.is_none() => {
                Some(SubscriptionStatusReadModel::new(
                    e.labour_id,
                    e.subscription_id,
                    e.subscriber_id.clone(),
                    SubscriberStatus::REQUESTED,
                    timestamp,
                ))
            }

            LabourEvent::SubscriberApproved(_) => {
                let mut subscription = model?;
                subscription.status = SubscriberStatus::SUBSCRIBED;
                Some(subscription)
            }

            LabourEvent::SubscriberRemoved(_) => {
                let mut subscription = model?;
                subscription.status = SubscriberStatus::REMOVED;
                Some(subscription)
            }

            LabourEvent::SubscriberBlocked(_) => {
                let mut subscription = model?;
                subscription.status = SubscriberStatus::BLOCKED;
                Some(subscription)
            }

            LabourEvent::SubscriberUnblocked(_) => {
                let mut subscription = model?;
                subscription.status = SubscriberStatus::REMOVED;
                Some(subscription)
            }

            LabourEvent::SubscriberUnsubscribed(_) => {
                let mut subscription = model?;
                subscription.status = SubscriberStatus::UNSUBSCRIBED;
                Some(subscription)
            }

            _ => model,
        }
    }
}

#[async_trait(?Send)]
impl AsyncProjector<LabourEvent> for SubscriptionStatusReadModelProjector {
    fn name(&self) -> &str {
        &self.name
    }

    async fn project_batch(&self, events: &[EventEnvelope<LabourEvent>]) -> Result<()> {
        if events.is_empty() {
            return Ok(());
        }

        let mut final_model = None;
        for envelope in events.iter() {
            final_model = self.project_event(final_model, envelope).await;
        }

        if let Some(model) = final_model {
            self.repository
                .overwrite(&model)
                .await
                .map_err(|err| anyhow!("Failed to persist SubscriptionStatusReadModel: {err}"))?;

            info!(
                projector = %self.name,
                labour_id = %model.labour_id,
                events_processed = events.len(),
                "Persisted read model after batch processing"
            );
        }

        Ok(())
    }
}
