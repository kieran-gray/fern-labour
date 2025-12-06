use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
pub enum NotificationChannel {
    #[strum(serialize = "EMAIL", serialize = "email")]
    EMAIL,
    #[strum(serialize = "SMS", serialize = "sms")]
    SMS,
    #[strum(serialize = "WHATSAPP", serialize = "whatsapp")]
    WHATSAPP,
}

impl std::fmt::Display for NotificationChannel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationChannel::EMAIL => write!(f, "EMAIL"),
            NotificationChannel::SMS => write!(f, "SMS"),
            NotificationChannel::WHATSAPP => write!(f, "WHATSAPP"),
        }
    }
}
