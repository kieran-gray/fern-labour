use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationDestination, NotificationPriority, NotificationTemplateData,
    RenderedContent,
};
use serde::{Deserialize, Serialize};
use std::{collections::HashMap, fmt::Debug};
use uuid::Uuid;

use fern_labour_event_sourcing_rs::{Event, StoredEvent};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum NotificationEvent {
    NotificationRequested {
        notification_id: Uuid,
        channel: NotificationChannel,
        destination: NotificationDestination,
        template_data: NotificationTemplateData,
        metadata: Option<HashMap<String, String>>,
        priority: NotificationPriority,
    },
    RenderedContentStored {
        notification_id: Uuid,
        rendered_content: RenderedContent,
    },
    NotificationDispatched {
        notification_id: Uuid,
        external_id: Option<String>,
    },
    NotificationDelivered {
        notification_id: Uuid,
        external_id: String,
    },
    NotificationDeliveryFailed {
        notification_id: Uuid,
        external_id: String,
        reason: Option<String>,
    },
}

impl NotificationEvent {
    pub fn into_stored_event(self) -> StoredEvent {
        let event_str = serde_json::to_string(&self).unwrap();

        StoredEvent {
            aggregate_id: self.aggregate_id().to_string(),
            event_type: self.event_type().to_string(),
            event_data: event_str,
            event_version: self.event_version(),
        }
    }

    pub fn from_stored_event(event: StoredEvent) -> Self {
        serde_json::from_str(&event.event_data).unwrap()
    }
}

impl Event for NotificationEvent {
    fn event_type(&self) -> &str {
        match self {
            NotificationEvent::NotificationRequested { .. } => "NotificationRequested",
            NotificationEvent::RenderedContentStored { .. } => "RenderedContentStored",
            NotificationEvent::NotificationDispatched { .. } => "NotificationDispatched",
            NotificationEvent::NotificationDelivered { .. } => "NotificationDelivered",
            NotificationEvent::NotificationDeliveryFailed { .. } => "NotificationDeliveryFailed",
        }
    }

    fn event_version(&self) -> i64 {
        1 // TODO: implement per event versioning
    }

    fn aggregate_id(&self) -> Uuid {
        match self {
            NotificationEvent::NotificationRequested {
                notification_id, ..
            } => *notification_id,
            NotificationEvent::RenderedContentStored {
                notification_id, ..
            } => *notification_id,
            NotificationEvent::NotificationDispatched {
                notification_id, ..
            } => *notification_id,
            NotificationEvent::NotificationDelivered {
                notification_id, ..
            } => *notification_id,
            NotificationEvent::NotificationDeliveryFailed {
                notification_id, ..
            } => *notification_id,
        }
    }
}
