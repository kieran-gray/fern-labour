use anyhow::{Context, Result, anyhow};
use chrono::Utc;
use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::{
    QueueMessage, QueueProducerTrait, ServiceCommand,
    service_clients::{DispatchClient, DispatchRequest, GenerationClient},
};
use tracing::info;
use uuid::Uuid;

use crate::durable_object::write_side::domain::NotificationCommand;

pub struct ServiceCommandProcessor {
    command_queue: Box<dyn QueueProducerTrait<Envelope = CommandEnvelope<QueueMessage>>>,
    generation_client: Box<dyn GenerationClient>,
    dispatch_client: Box<dyn DispatchClient>,
}

impl ServiceCommandProcessor {
    pub fn create(
        command_queue: Box<dyn QueueProducerTrait<Envelope = CommandEnvelope<QueueMessage>>>,
        generation_client: Box<dyn GenerationClient>,
        dispatch_client: Box<dyn DispatchClient>,
    ) -> Self {
        Self {
            command_queue,
            generation_client,
            dispatch_client,
        }
    }

    pub async fn handle(&self, command: ServiceCommand) -> Result<()> {
        let aggregate_id = command.notification_id();
        let correlation_id = Uuid::now_v7();
        let message = QueueMessage::Service(command);

        let envelope = CommandEnvelope::enrich(
            message,
            aggregate_id,
            correlation_id,
            correlation_id,
            "notification".to_string(),
            Utc::now(),
        );

        self.command_queue
            .publish(envelope)
            .await
            .context("Failed to send service command to queue")
    }

    pub async fn handle_priority(&self, command: ServiceCommand) -> Result<NotificationCommand> {
        match command {
            ServiceCommand::RenderNotification {
                notification_id,
                channel,
                template_data,
            } => {
                info!(
                    notification_id = %notification_id,
                    channel = %channel,
                    "Calling generation service directly (priority)"
                );

                let rendered_content = self
                    .generation_client
                    .render(notification_id, channel.clone(), template_data)
                    .await
                    .map_err(|err| anyhow!("Failed to render notification content: {err}"))?;

                Ok(NotificationCommand::StoreRenderedContent {
                    notification_id,
                    rendered_content,
                })
            }
            ServiceCommand::DispatchNotification {
                notification_id,
                channel,
                destination,
                rendered_content,
            } => {
                info!(
                    notification_id = %notification_id,
                    channel = %channel,
                    destination = %destination,
                    "Calling dispatch service directly"
                );

                let request = DispatchRequest {
                    notification_id,
                    channel,
                    destination,
                    rendered_content,
                    idempotency_key: format!("notification-{}", notification_id),
                };

                let external_id = self
                    .dispatch_client
                    .dispatch(request)
                    .await
                    .context("Failed to dispatch notification")?;

                Ok(NotificationCommand::MarkAsDispatched {
                    notification_id,
                    external_id,
                })
            }
        }
    }
}
