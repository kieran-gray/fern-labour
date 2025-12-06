use std::{collections::HashMap, str::FromStr};

use anyhow::{Context, Result};
use chrono::{DateTime, Utc};
use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationDestination, NotificationPriority, NotificationTemplateData,
};
use serde::{Deserialize, Serialize};
use strum::VariantNames;
use uuid::Uuid;

use crate::durable_object::write_side::domain::NotificationCommand;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlanLabourDTO {
    pub first_labour: bool,
    pub due_date: DateTime<Utc>,
    pub labour_name: Option<String>,
}

impl PlanLabourDTO {
    pub fn into_domain(self, labour_id: Uuid) -> Result<NotificationCommand> {
        let channel = NotificationChannel::from_str(&self.channel).with_context(|| {
            format!(
                "Invalid notification channel: '{}'. Valid channels are: {}",
                self.channel,
                NotificationChannel::VARIANTS.join(", ")
            )
        })?;

        let destination =
            NotificationDestination::from_string_and_channel(self.destination.clone(), &channel)
                .with_context(|| {
                    format!(
                        "Invalid destination '{}' for channel '{}'. Expected format: {}",
                        self.destination,
                        channel,
                        match channel {
                            NotificationChannel::EMAIL => "valid email address",
                            NotificationChannel::SMS => "valid phone number (E.164 format)",
                            NotificationChannel::WHATSAPP => "valid phone number (E.164 format)",
                        }
                    )
                })?;

        Ok(NotificationCommand::RequestNotification {
            notification_id,
            channel,
            destination,
            template_data: self.template_data,
            metadata: self.metadata,
            priority: self.priority,
        })
    }
}
