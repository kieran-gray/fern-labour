use std::{collections::HashMap, fmt::Debug};

use serde::{Deserialize, Serialize};
use uuid::Uuid;

use fern_labour_event_sourcing_rs::Aggregate;

use crate::durable_object::write_side::domain::{
    NotificationCommand, NotificationError, NotificationEvent,
};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Labour {
    id: Uuid,
    status: NotificationStatus,
    channel: NotificationChannel,
    destination: NotificationDestination,
    template_data: NotificationTemplateData,
    metadata: Option<HashMap<String, String>>,
    priority: NotificationPriority,
    external_id: Option<String>,
    rendered_content: Option<RenderedContent>,
    failure_reason: Option<String>,
}

impl Labour {
    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn status(&self) -> &NotificationStatus {
        &self.status
    }

    pub fn channel(&self) -> &NotificationChannel {
        &self.channel
    }

    pub fn destination(&self) -> &NotificationDestination {
        &self.destination
    }

    pub fn template_data(&self) -> &NotificationTemplateData {
        &self.template_data
    }

    pub fn metadata(&self) -> Option<&HashMap<String, String>> {
        self.metadata.as_ref()
    }

    pub fn external_id(&self) -> Option<&String> {
        self.external_id.as_ref()
    }

    pub fn rendered_content(&self) -> Option<&RenderedContent> {
        self.rendered_content.as_ref()
    }

    pub fn failure_reason(&self) -> Option<&String> {
        self.failure_reason.as_ref()
    }

    pub fn priority(&self) -> &NotificationPriority {
        &self.priority
    }

    pub fn is_priority(&self) -> bool {
        self.priority.is_high()
    }
}

impl Aggregate for Labour {
    type Command = NotificationCommand;
    type Error = NotificationError;
    type Event = NotificationEvent;

    fn aggregate_id(&self) -> String {
        self.id.to_string()
    }

    fn apply(&mut self, event: &Self::Event) {
        match event {
            NotificationEvent::NotificationRequested {
                notification_id,
                channel,
                destination,
                template_data,
                metadata,
                priority,
            } => {
                self.id = *notification_id;
                self.channel = channel.clone();
                self.destination = destination.clone();
                self.template_data = template_data.clone();
                self.metadata = metadata.clone();
                self.priority = *priority;
                self.status = NotificationStatus::REQUESTED;
            }
            NotificationEvent::RenderedContentStored {
                rendered_content, ..
            } => {
                self.rendered_content = Some(rendered_content.clone());
                self.status = NotificationStatus::RENDERED;
            }
            NotificationEvent::NotificationDispatched { external_id, .. } => {
                self.external_id = external_id.clone();
                self.status = NotificationStatus::SENT;
            }
            NotificationEvent::NotificationDelivered { .. } => {
                self.status = NotificationStatus::DELIVERED;
            }
            NotificationEvent::NotificationDeliveryFailed { reason, .. } => {
                self.status = NotificationStatus::FAILED;
                self.failure_reason = reason.clone();
            }
        }
    }

    fn handle_command(
        state: Option<&Self>,
        command: Self::Command,
    ) -> std::result::Result<Vec<Self::Event>, Self::Error> {
        let events = match command {
            NotificationCommand::RequestNotification {
                notification_id,
                channel,
                destination,
                template_data,
                metadata,
                priority,
            } => {
                if state.is_some() {
                    return Err(NotificationError::AlreadyExists);
                }
                if !destination.matches_channel(&channel) {
                    return Err(NotificationError::ValidationError(format!(
                        "Destination channel {} does not match notification channel {}",
                        destination.channel(),
                        channel
                    )));
                }

                vec![NotificationEvent::NotificationRequested {
                    notification_id,
                    channel: channel.clone(),
                    destination,
                    template_data: template_data.clone(),
                    metadata,
                    priority,
                }]
            }
            NotificationCommand::StoreRenderedContent {
                notification_id,
                rendered_content,
            } => {
                let Some(notification) = &state else {
                    return Err(NotificationError::NotFound);
                };

                if notification.status != NotificationStatus::REQUESTED {
                    return Err(NotificationError::InvalidStateTransition(
                        "Cannot store template for notification not in REQUESTED state".to_string(),
                    ));
                }

                if rendered_content.channel() != notification.channel.to_string() {
                    return Err(NotificationError::ValidationError(
                        "Rendered content channel doesn't match notification channel".to_string(),
                    ));
                }

                vec![NotificationEvent::RenderedContentStored {
                    notification_id,
                    rendered_content: rendered_content.clone(),
                }]
            }
            NotificationCommand::MarkAsDispatched {
                notification_id,
                external_id,
            } => {
                let Some(notification) = &state else {
                    return Err(NotificationError::NotFound);
                };

                if ![NotificationStatus::RENDERED, NotificationStatus::FAILED]
                    .contains(&notification.status)
                {
                    return Err(NotificationError::InvalidStateTransition(
                        "Cannot dispatch notification in current state".to_string(),
                    ));
                }

                vec![NotificationEvent::NotificationDispatched {
                    notification_id,
                    external_id,
                }]
            }
            NotificationCommand::MarkAsDelivered { notification_id } => {
                let Some(notification) = &state else {
                    return Err(NotificationError::NotFound);
                };

                if notification.status != NotificationStatus::SENT {
                    return Err(NotificationError::InvalidStateTransition(
                        "Cannot mark as delivered if not in SENT state".to_string(),
                    ));
                }

                let Some(external_id) = notification.external_id.clone() else {
                    return Err(NotificationError::InvalidStateTransition(
                        "Cannot mark as delivered, no external ID".to_string(),
                    ));
                };

                vec![NotificationEvent::NotificationDelivered {
                    notification_id,
                    external_id,
                }]
            }
            NotificationCommand::MarkAsFailed {
                notification_id,
                reason,
            } => {
                let Some(notification) = &state else {
                    return Err(NotificationError::NotFound);
                };

                let Some(external_id) = notification.external_id.clone() else {
                    return Err(NotificationError::InvalidStateTransition(
                        "Cannot mark as failed, no external ID".to_string(),
                    ));
                };

                if NotificationStatus::SENT != notification.status {
                    return Err(NotificationError::InvalidStateTransition(
                        "Can only mark as failed from SENT state".to_string(),
                    ));
                }

                vec![NotificationEvent::NotificationDeliveryFailed {
                    notification_id,
                    external_id,
                    reason,
                }]
            }
        };
        Ok(events)
    }

    fn from_events(events: &[Self::Event]) -> Option<Self> {
        let mut notification = match events.first() {
            Some(NotificationEvent::NotificationRequested {
                notification_id,
                channel,
                destination,
                template_data,
                metadata,
                priority,
            }) => Labour {
                id: *notification_id,
                status: NotificationStatus::REQUESTED,
                channel: channel.clone(),
                destination: destination.clone(),
                template_data: template_data.clone(),
                metadata: metadata.clone(),
                priority: *priority,
                external_id: None,
                rendered_content: None,
                failure_reason: None,
            },
            _ => return None,
        };

        for event in events.iter().skip(1) {
            notification.apply(event);
        }

        Some(notification)
    }
}
