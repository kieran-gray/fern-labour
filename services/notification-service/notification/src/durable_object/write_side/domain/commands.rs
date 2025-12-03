use std::{collections::HashMap, str::FromStr};

use anyhow::{Context, Result};
use fern_labour_notifications_shared::{
    InternalCommand, PublicCommand,
    value_objects::{
        NotificationChannel, NotificationDestination, NotificationPriority,
        NotificationTemplateData, RenderedContent,
    },
};
use serde::{Deserialize, Serialize};
use strum::VariantNames;
use uuid::Uuid;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum NotificationCommand {
    RequestNotification {
        notification_id: Uuid,
        channel: NotificationChannel,
        destination: NotificationDestination,
        template_data: NotificationTemplateData,
        metadata: Option<HashMap<String, String>>,
        priority: NotificationPriority,
    },
    StoreRenderedContent {
        notification_id: Uuid,
        rendered_content: RenderedContent,
    },
    MarkAsDispatched {
        notification_id: Uuid,
        external_id: Option<String>,
    },
    MarkAsDelivered {
        notification_id: Uuid,
    },
    MarkAsFailed {
        notification_id: Uuid,
        reason: Option<String>,
    },
}

impl TryFrom<(PublicCommand, Uuid)> for NotificationCommand {
    type Error = anyhow::Error;
    fn try_from((command, notification_id): (PublicCommand, Uuid)) -> Result<Self> {
        match command {
            PublicCommand::RequestNotification {
                channel,
                destination,
                template_data,
                metadata,
                priority,
            } => {
                let channel = NotificationChannel::from_str(&channel).with_context(|| {
                    format!(
                        "Invalid notification channel: '{}'. Valid channels are: {}",
                        channel,
                        NotificationChannel::VARIANTS.join(", ")
                    )
                })?;

                let destination =
                    NotificationDestination::from_string_and_channel(destination.clone(), &channel)
                        .with_context(|| {
                            format!(
                                "Invalid destination '{}' for channel '{}'. Expected format: {}",
                                destination,
                                channel,
                                match channel {
                                    NotificationChannel::EMAIL => "valid email address",
                                    NotificationChannel::SMS => "valid phone number (E.164 format)",
                                    NotificationChannel::WHATSAPP =>
                                        "valid phone number (E.164 format)",
                                }
                            )
                        })?;
                Ok(NotificationCommand::RequestNotification {
                    notification_id,
                    channel,
                    destination,
                    template_data,
                    metadata,
                    priority,
                })
            }
        }
    }
}

impl From<InternalCommand> for NotificationCommand {
    fn from(cmd: InternalCommand) -> Self {
        match cmd {
            InternalCommand::StoreRenderedContent {
                notification_id,
                rendered_content,
            } => NotificationCommand::StoreRenderedContent {
                notification_id,
                rendered_content,
            },
            InternalCommand::MarkAsDispatched {
                notification_id,
                external_id,
            } => NotificationCommand::MarkAsDispatched {
                notification_id,
                external_id,
            },
            InternalCommand::MarkAsDelivered { notification_id } => {
                NotificationCommand::MarkAsDelivered { notification_id }
            }
            InternalCommand::MarkAsFailed {
                notification_id,
                reason,
            } => NotificationCommand::MarkAsFailed {
                notification_id,
                reason,
            },
        }
    }
}
