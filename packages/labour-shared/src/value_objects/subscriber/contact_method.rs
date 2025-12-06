use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
pub enum SubscriberContactMethod {
    #[strum(serialize = "EMAIL", serialize = "email")]
    EMAIL,
    #[strum(serialize = "SMS", serialize = "sms")]
    SMS,
    #[strum(serialize = "WHATSAPP", serialize = "whatsapp")]
    WHATSAPP,
}

impl std::fmt::Display for SubscriberContactMethod {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SubscriberContactMethod::EMAIL => write!(f, "EMAIL"),
            SubscriberContactMethod::SMS => write!(f, "SMS"),
            SubscriberContactMethod::WHATSAPP => write!(f, "WHATSAPP"),
        }
    }
}
