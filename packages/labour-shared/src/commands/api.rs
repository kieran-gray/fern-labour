use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::{
    AdminCommand, ContractionCommand, LabourCommand, LabourUpdateCommand, SubscriberCommand,
    SubscriptionCommand,
};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum ApiCommand {
    #[serde(rename = "Admin")]
    Admin(AdminCommand),

    #[serde(rename = "Contraction")]
    Contraction(ContractionCommand),

    #[serde(rename = "Labour")]
    Labour(LabourCommand),

    #[serde(rename = "LabourUpdate")]
    LabourUpdate(LabourUpdateCommand),

    #[serde(rename = "Subscriber")]
    Subscriber(SubscriberCommand),

    #[serde(rename = "Subscription")]
    Subscription(SubscriptionCommand),
}

impl ApiCommand {
    pub fn labour_id(&self) -> Uuid {
        match self {
            Self::Admin(cmd) => cmd.labour_id(),
            Self::Contraction(cmd) => cmd.labour_id(),
            Self::Labour(cmd) => cmd.labour_id(),
            Self::LabourUpdate(cmd) => cmd.labour_id(),
            Self::Subscriber(cmd) => cmd.labour_id(),
            Self::Subscription(cmd) => cmd.labour_id(),
        }
    }
}
