use anyhow::{Context, Result};
use async_trait::async_trait;
use tracing::info;

use fern_labour_event_sourcing_rs::{AsyncProjector, AsyncRepositoryTrait, EventEnvelope};

use crate::{
    durable_object::write_side::domain::NotificationEvent,
    read_models::notification_status::read_model::NotificationStatus,
};

pub struct NotificationStatusProjector {
    name: String,
    repository: Box<dyn AsyncRepositoryTrait<NotificationStatus>>,
}

impl NotificationStatusProjector {
    pub fn create(repository: Box<dyn AsyncRepositoryTrait<NotificationStatus>>) -> Self {
        Self {
            name: "NotificationStatusProjector".to_string(),
            repository,
        }
    }

    fn project_event(
        &self,
        model: Option<NotificationStatus>,
        envelope: &EventEnvelope<NotificationEvent>,
    ) -> Option<NotificationStatus> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            NotificationEvent::NotificationRequested { .. } if model.is_none() => Some(
                NotificationStatus::new(metadata.aggregate_id, metadata.user_id.clone(), timestamp),
            ),

            NotificationEvent::RenderedContentStored { .. } => {
                let mut detail = model?;
                detail.status = "RENDERED".to_string();
                detail.updated_at = timestamp;
                Some(detail)
            }

            NotificationEvent::NotificationDispatched { .. } => {
                let mut detail = model?;
                detail.status = "SENT".to_string();
                detail.updated_at = timestamp;
                Some(detail)
            }

            NotificationEvent::NotificationDelivered { .. } => {
                let mut detail = model?;
                detail.status = "DELIVERED".to_string();
                detail.updated_at = timestamp;
                Some(detail)
            }

            NotificationEvent::NotificationDeliveryFailed { .. } => {
                let mut detail = model?;
                detail.status = "FAILED".to_string();
                detail.updated_at = timestamp;
                Some(detail)
            }

            _ => model,
        }
    }
}

#[async_trait(?Send)]
impl AsyncProjector<NotificationEvent> for NotificationStatusProjector {
    fn name(&self) -> &str {
        &self.name
    }

    async fn project_batch(&self, events: &[EventEnvelope<NotificationEvent>]) -> Result<()> {
        if events.is_empty() {
            return Ok(());
        }

        let final_model = events
            .iter()
            .fold(None, |model, envelope| self.project_event(model, envelope));

        if let Some(model) = final_model {
            self.repository
                .overwrite(&model)
                .await
                .context("Failed to persist NotificationStatus")?;

            info!(
                projector = %self.name,
                notification_id = %model.notification_id,
                events_processed = events.len(),
                "Persisted read model after batch processing"
            );
        }

        Ok(())
    }
}
