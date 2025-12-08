use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::value_objects::SubscriberRole;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum SubscriptionCommand {
    #[serde(rename = "ApproveSubscriber")]
    ApproveSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },

    #[serde(rename = "RemoveSubscriber")]
    RemoveSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },

    #[serde(rename = "BlockSubscriber")]
    BlockSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },

    #[serde(rename = "UnblockSubscriber")]
    UnblockSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },

    #[serde(rename = "UpdateSubscriberRole")]
    UpdateSubscriberRole {
        labour_id: Uuid,
        subscription_id: Uuid,
        role: SubscriberRole,
    },
}

impl SubscriptionCommand {
    pub fn labour_id(&self) -> Uuid {
        match self {
            SubscriptionCommand::ApproveSubscriber { labour_id, .. } => *labour_id,
            SubscriptionCommand::RemoveSubscriber { labour_id, .. } => *labour_id,
            SubscriptionCommand::BlockSubscriber { labour_id, .. } => *labour_id,
            SubscriptionCommand::UnblockSubscriber { labour_id, .. } => *labour_id,
            SubscriptionCommand::UpdateSubscriberRole { labour_id, .. } => *labour_id,
        }
    }
}
