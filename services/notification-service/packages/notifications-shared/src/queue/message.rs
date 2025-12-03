use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::commands::{
    admin::AdminCommand, api::PublicCommand, internal::InternalCommand, service::ServiceCommand,
};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "message_type", content = "command")]
pub enum QueueMessage {
    #[serde(rename = "public")]
    Public(PublicCommand),

    #[serde(rename = "internal")]
    Internal(InternalCommand),

    #[serde(rename = "service")]
    Service(ServiceCommand),

    #[serde(rename = "admin")]
    Admin(AdminCommand),
}

impl QueueMessage {
    pub fn notification_id(&self) -> Uuid {
        match self {
            QueueMessage::Public(_) => {
                panic!("Public commands don't have a notification_id - generate one before queuing")
            }
            QueueMessage::Internal(cmd) => match cmd {
                InternalCommand::StoreRenderedContent {
                    notification_id, ..
                } => *notification_id,
                InternalCommand::MarkAsDispatched {
                    notification_id, ..
                } => *notification_id,
                InternalCommand::MarkAsDelivered { notification_id } => *notification_id,
                InternalCommand::MarkAsFailed {
                    notification_id, ..
                } => *notification_id,
            },
            QueueMessage::Service(cmd) => cmd.notification_id(),
            QueueMessage::Admin(cmd) => match cmd {
                AdminCommand::RebuildReadModels { aggregate_id } => *aggregate_id,
            },
        }
    }

    pub fn is_service_command(&self) -> bool {
        matches!(self, QueueMessage::Service(_))
    }

    pub fn is_internal_callback(&self) -> bool {
        matches!(self, QueueMessage::Internal(_))
    }

    pub fn command_name(&self) -> &'static str {
        match self {
            QueueMessage::Public(PublicCommand::RequestNotification { .. }) => {
                "PublicCommand::RequestNotification"
            }
            QueueMessage::Internal(InternalCommand::StoreRenderedContent { .. }) => {
                "InternalCommand::StoreRenderedContent"
            }
            QueueMessage::Internal(InternalCommand::MarkAsDispatched { .. }) => {
                "InternalCommand::MarkAsDispatched"
            }
            QueueMessage::Internal(InternalCommand::MarkAsDelivered { .. }) => {
                "InternalCommand::MarkAsDelivered"
            }
            QueueMessage::Internal(InternalCommand::MarkAsFailed { .. }) => {
                "InternalCommand::MarkAsFailed"
            }
            QueueMessage::Service(ServiceCommand::RenderNotification { .. }) => {
                "ServiceCommand::RenderNotification"
            }
            QueueMessage::Service(ServiceCommand::DispatchNotification { .. }) => {
                "ServiceCommand::DispatchNotification"
            }
            QueueMessage::Admin(AdminCommand::RebuildReadModels { .. }) => {
                "AdminCommand::RebuildReadModels"
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::value_objects::{NotificationChannel, NotificationTemplateData};
    use uuid::Uuid;

    #[test]
    fn test_queue_message_serialization() {
        let notification_id = Uuid::now_v7();
        let msg = QueueMessage::Service(ServiceCommand::RenderNotification {
            notification_id,
            channel: NotificationChannel::EMAIL,
            template_data: NotificationTemplateData::ContactUs {
                name: "Test".to_string(),
            },
        });

        let json = serde_json::to_string(&msg).unwrap();
        let deserialized: QueueMessage = serde_json::from_str(&json).unwrap();

        assert!(matches!(deserialized, QueueMessage::Service(_)));
        assert_eq!(deserialized.notification_id(), notification_id);
    }

    #[test]
    fn test_message_type_checks() {
        let notification_id = Uuid::now_v7();

        let service_msg = QueueMessage::Service(ServiceCommand::RenderNotification {
            notification_id,
            channel: NotificationChannel::EMAIL,
            template_data: NotificationTemplateData::ContactUs {
                name: "Test".to_string(),
            },
        });
        assert!(service_msg.is_service_command());
        assert!(!service_msg.is_internal_callback());

        let internal_msg = QueueMessage::Internal(InternalCommand::MarkAsDispatched {
            notification_id,
            external_id: Some("ext-123".to_string()),
        });
        assert!(!internal_msg.is_service_command());
        assert!(internal_msg.is_internal_callback());
    }
}
