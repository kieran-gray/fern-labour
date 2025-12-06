use serde::{Deserialize, Serialize};

use crate::{AdminCommand, ContractionCommand, LabourCommand, LabourUpdateCommand, SubscriberCommand, SubscriptionCommand};


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
