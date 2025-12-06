use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
#[allow(non_camel_case_types)]
pub enum SubscriberStatus {
    #[strum(serialize = "SUBSCRIBED", serialize = "subscribed")]
    SUBSCRIBED,
    #[strum(serialize = "UNSUBSCRIBED", serialize = "unsubscribed")]
    UNSUBSCRIBED,
    #[strum(serialize = "REQUESTED", serialize = "requested")]
    REQUESTED,
    #[strum(serialize = "REMOVED", serialize = "removed")]
    REMOVED,
    #[strum(serialize = "BLOCKED", serialize = "blocked")]
    BLOCKED,
}

impl std::fmt::Display for SubscriberStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SubscriberStatus::SUBSCRIBED => write!(f, "SUBSCRIBED"),
            SubscriberStatus::UNSUBSCRIBED => write!(f, "UNSUBSCRIBED"),
            SubscriberStatus::REQUESTED => write!(f, "REQUESTED"),
            SubscriberStatus::REMOVED => write!(f, "REMOVED"),
            SubscriberStatus::BLOCKED => write!(f, "BLOCKED"),
        }
    }
}
