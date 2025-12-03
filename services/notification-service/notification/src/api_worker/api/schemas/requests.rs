use std::{collections::HashMap, str::FromStr};

use anyhow::{Context, Result};
use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationDestination, NotificationPriority, NotificationTemplateData,
};
use serde::{Deserialize, Serialize};
use strum::VariantNames;
use uuid::Uuid;

use crate::durable_object::write_side::domain::NotificationCommand;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RequestNotificationDto {
    pub channel: String,
    pub destination: String,
    pub template_data: NotificationTemplateData,
    #[serde(default)]
    pub metadata: Option<HashMap<String, String>>,
    #[serde(default)]
    pub priority: NotificationPriority,
}

impl RequestNotificationDto {
    pub fn try_into_domain(self, notification_id: Uuid) -> Result<NotificationCommand> {
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn converts_valid_email_request() {
        let dto = RequestNotificationDto {
            channel: "EMAIL".to_string(),
            destination: "user@example.com".to_string(),
            template_data: NotificationTemplateData::ContactUs {
                name: "TEST".to_string(),
            },
            metadata: None,
            priority: NotificationPriority::Normal,
        };

        let notification_id = Uuid::now_v7();
        let result = dto.try_into_domain(notification_id);

        assert!(result.is_ok());
        match result.unwrap() {
            NotificationCommand::RequestNotification {
                notification_id: id,
                channel,
                destination,
                ..
            } => {
                assert_eq!(id, notification_id);
                assert_eq!(channel.to_string(), "EMAIL");
                assert_eq!(destination.to_string(), "user@example.com");
            }
            _ => panic!("Expected RequestNotification variant"),
        }
    }

    #[test]
    fn returns_error_for_invalid_channel() {
        let dto = RequestNotificationDto {
            channel: "INVALID_CHANNEL".to_string(),
            destination: "test".to_string(),
            template_data: NotificationTemplateData::ContactUs {
                name: "TEST".to_string(),
            },
            metadata: None,
            priority: NotificationPriority::Normal,
        };

        let result = dto.try_into_domain(Uuid::now_v7());
        assert!(result.is_err());
        let err_msg = result.unwrap_err().to_string();
        assert!(err_msg.contains("Invalid notification channel"));
        assert!(err_msg.contains("INVALID_CHANNEL"));
    }

    #[test]
    fn returns_error_for_invalid_email() {
        let dto = RequestNotificationDto {
            channel: "EMAIL".to_string(),
            destination: "not-an-email".to_string(),
            template_data: NotificationTemplateData::ContactUs {
                name: "TEST".to_string(),
            },
            metadata: None,
            priority: NotificationPriority::Normal,
        };

        let result = dto.try_into_domain(Uuid::now_v7());
        assert!(result.is_err());
        let err_msg = result.unwrap_err().to_string();
        assert!(err_msg.contains("Invalid destination"));
        assert!(err_msg.contains("EMAIL"));
    }

    #[test]
    fn includes_metadata_and_priority() {
        let mut metadata = HashMap::new();
        metadata.insert("key".to_string(), "value".to_string());

        let dto = RequestNotificationDto {
            channel: "EMAIL".to_string(),
            destination: "user@example.com".to_string(),
            template_data: NotificationTemplateData::ContactUs {
                name: "TEST".to_string(),
            },
            metadata: Some(metadata.clone()),
            priority: NotificationPriority::High,
        };

        let result = dto.try_into_domain(Uuid::now_v7()).unwrap();
        match result {
            NotificationCommand::RequestNotification {
                metadata: m,
                priority: p,
                ..
            } => {
                assert_eq!(m, Some(metadata));
                assert_eq!(p, NotificationPriority::High);
            }
            _ => panic!("Expected RequestNotification variant"),
        }
    }
}
