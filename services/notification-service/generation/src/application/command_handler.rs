use anyhow::{Context, Result};
use chrono::Utc;
use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::{InternalCommand, ServiceCommand};
use tracing::{debug, error, info};
use uuid::Uuid;
use worker::Queue;

use crate::application::{exceptions::AppError, template_engine::TemplateEngineTrait};

pub struct NotificationCommandHandler {
    pub template_engine: Box<dyn TemplateEngineTrait>,
    pub command_bus: Queue,
}

impl NotificationCommandHandler {
    pub fn create(template_engine: Box<dyn TemplateEngineTrait>, command_bus: Queue) -> Self {
        Self {
            template_engine,
            command_bus,
        }
    }

    pub async fn consume_event(&self, command: &ServiceCommand, user_id: &str) -> Result<()> {
        match command {
            ServiceCommand::RenderNotification {
                notification_id,
                channel,
                template_data,
            } => {
                debug!("RenderNotificationContent event received");
                let rendered_template = self
                    .template_engine
                    .render_content(channel.clone(), template_data.clone())
                    .map_err(|e| {
                        error!(error = %e, "Failed to render notification content");
                        anyhow::Error::new(AppError::ConsumerError(format!(
                            "Failed to render notification content: {e}"
                        )))
                    })?;

                let command = InternalCommand::StoreRenderedContent {
                    notification_id: *notification_id,
                    rendered_content: rendered_template,
                };

                let new_envelope = CommandEnvelope::enrich(
                    command,
                    *notification_id,
                    Uuid::now_v7(),
                    Uuid::now_v7(),
                    user_id.to_string(),
                    Utc::now(),
                );

                info!(
                    notification_id = %notification_id,
                    command_id = %new_envelope.metadata.command_id,
                    "Publishing StoreRenderedTemplate command to queue"
                );

                let json_string =
                    serde_json::to_string(&new_envelope).context("Failed to serialize command")?;

                self.command_bus
                    .send(&json_string)
                    .await
                    .context("Failed to publish to queue")?;

                Ok(())
            }
            _ => {
                debug!("Skipping event.");
                Ok(())
            }
        }
    }
}
