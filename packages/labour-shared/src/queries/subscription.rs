use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum SubscriptionQuery {
    #[serde(rename = "GetSubscriptionToken")]
    GetSubscriptionToken {
        labour_id: Uuid,
    },
    GetLabourSubscriptions {
        labour_id: Uuid,
    },
    GetUserSubscription {
        labour_id: Uuid,
    }
}

impl SubscriptionQuery {
    pub fn labour_id(&self) -> Uuid {
        match self {
            SubscriptionQuery::GetSubscriptionToken { labour_id } => *labour_id,
            SubscriptionQuery::GetLabourSubscriptions { labour_id } => *labour_id,
            SubscriptionQuery::GetUserSubscription { labour_id } => *labour_id,
        }
    }
}
