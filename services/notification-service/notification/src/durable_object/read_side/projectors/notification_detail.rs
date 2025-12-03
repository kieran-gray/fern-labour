use anyhow::{Context, Result};
use async_trait::async_trait;
use tracing::info;

use fern_labour_event_sourcing_rs::{EventEnvelope, Projector, RepositoryTrait};

use crate::{
    durable_object::write_side::domain::NotificationEvent,
    read_models::notification_detail::read_model::NotificationDetail,
};

pub struct NotificationDetailProjector {
    name: String,
    repository: Box<dyn RepositoryTrait<NotificationDetail>>,
}

impl NotificationDetailProjector {
    pub fn create(repository: Box<dyn RepositoryTrait<NotificationDetail>>) -> Self {
        Self {
            name: "NotificationDetailProjector".to_string(),
            repository,
        }
    }

    fn project_event(
        &self,
        model: Option<NotificationDetail>,
        envelope: &EventEnvelope<NotificationEvent>,
    ) -> Option<NotificationDetail> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            NotificationEvent::NotificationRequested {
                channel,
                destination,
                template_data,
                ..
            } if model.is_none() => Some(NotificationDetail::new(
                metadata.aggregate_id,
                metadata.user_id.clone(),
                channel.to_string(),
                destination.to_string(),
                template_data.template().to_string(),
                timestamp,
            )),

            NotificationEvent::RenderedContentStored {
                rendered_content, ..
            } => {
                let mut detail = model?;
                detail.status = "RENDERED".to_string();
                detail.rendered_content = Some(rendered_content.clone());
                detail.updated_at = timestamp;
                Some(detail)
            }

            NotificationEvent::NotificationDispatched { external_id, .. } => {
                let mut detail = model?;
                detail.status = "SENT".to_string();
                detail.external_id = external_id.clone();
                detail.dispatched_at = Some(timestamp);
                detail.updated_at = timestamp;
                Some(detail)
            }

            NotificationEvent::NotificationDelivered { .. } => {
                let mut detail = model?;
                detail.status = "DELIVERED".to_string();
                detail.delivered_at = Some(timestamp);
                detail.updated_at = timestamp;
                Some(detail)
            }

            NotificationEvent::NotificationDeliveryFailed { .. } => {
                let mut detail = model?;
                detail.status = "FAILED".to_string();
                detail.failed_at = Some(timestamp);
                detail.updated_at = timestamp;
                Some(detail)
            }

            _ => model,
        }
    }
}

#[async_trait(?Send)]
impl Projector<NotificationEvent> for NotificationDetailProjector {
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
                .context("Failed to persist NotificationDetail")?;

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
