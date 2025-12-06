use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::value_objects::{SubscriberAccessLevel, SubscriberContactMethod};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum SubscriberCommand {
    #[serde(rename = "RequestAccess")]
    RequestAccess {
        labour_id: Uuid,
        token: String,
    },

    #[serde(rename = "Unsubscribe")]
    Unsubscribe { labour_id: Uuid },

    #[serde(rename = "UpdateNotificationMethods")]
    UpdateNotificationMethods { labour_id: Uuid, notification_methods: Vec<SubscriberContactMethod> },

    #[serde(rename = "UpdateAccessLevel")]
    UpdateAccessLevel {
        labour_id: Uuid,
        access_level: SubscriberAccessLevel,
    },
}

impl SubscriberCommand {
    pub fn labour_id(&self) -> Option<Uuid> {
        match self {
            SubscriberCommand::RequestAccess { labour_id, .. } => Some(*labour_id),
            SubscriberCommand::Unsubscribe { labour_id, .. } => Some(*labour_id),
            SubscriberCommand::UpdateNotificationMethods { labour_id, .. } => Some(*labour_id),
            SubscriberCommand::UpdateAccessLevel { labour_id, .. } => Some(*labour_id),
        }
    }
}
