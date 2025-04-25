use serde::{Deserialize, Serialize};
use sqlx::Type;
use strum_macros::EnumString;

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, Type, PartialEq)]
#[sqlx(type_name = "notification_type", rename_all = "lowercase")]
pub enum NotificationType {
    #[strum(serialize = "EMAIL", serialize = "email")]
    EMAIL,
    #[strum(serialize = "SMS", serialize = "sms")]
    SMS,
}

impl std::fmt::Display for NotificationType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationType::EMAIL => write!(f, "EMAIL"),
            NotificationType::SMS => write!(f, "SMS"),
        }
    }
}

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, Type, PartialEq)]
#[sqlx(type_name = "notification_status", rename_all = "lowercase")]
pub enum NotificationStatus {
    #[strum(serialize = "CREATED", serialize = "created")]
    CREATED,
    #[strum(serialize = "SENT", serialize = "sent")]
    SENT,
    #[strum(serialize = "FAILURE", serialize = "failure")]
    FAILURE,
    #[strum(serialize = "SUCCESS", serialize = "success")]
    SUCCESS,
}

impl std::fmt::Display for NotificationStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationStatus::CREATED => write!(f, "CREATED"),
            NotificationStatus::SENT => write!(f, "SENT"),
            NotificationStatus::FAILURE => write!(f, "FAILURE"),
            NotificationStatus::SUCCESS => write!(f, "SUCCESS"),
        }
    }
}

#[allow(non_camel_case_types)]
#[derive(Debug, Clone, Deserialize, Serialize, EnumString, Type, PartialEq)]
#[sqlx(type_name = "notification_template", rename_all = "lowercase")]
pub enum NotificationTemplate {
    #[strum(serialize = "LABOUR_UPDATE", serialize = "labour_update")]
    LABOUR_UPDATE,
    #[strum(serialize = "LABOUR_INVITE", serialize = "labour_invite")]
    LABOUR_INVITE,
    #[strum(serialize = "SUBSCRIBER_INVITE", serialize = "subscriber_invite")]
    SUBSCRIBER_INVITE,
    #[strum(
        serialize = "CONTACT_US_SUBMISSION",
        serialize = "contact_us_submission"
    )]
    CONTACT_US_SUBMISSION,
}

impl std::fmt::Display for NotificationTemplate {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationTemplate::LABOUR_UPDATE => write!(f, "LABOUR_UPDATE"),
            NotificationTemplate::LABOUR_INVITE => write!(f, "LABOUR_INVITE"),
            NotificationTemplate::SUBSCRIBER_INVITE => write!(f, "SUBSCRIBER_INVITE"),
            NotificationTemplate::CONTACT_US_SUBMISSION => write!(f, "CONTACT_US_SUBMISSION"),
        }
    }
}
