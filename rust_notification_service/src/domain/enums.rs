use serde::{Deserialize, Serialize};

use super::exceptions::{
    InvalidNotificationStatus, InvalidNotificationTemplate, InvalidNotificationType,
};

#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum NotificationType {
    EMAIL,
    SMS,
}

impl std::str::FromStr for NotificationType {
    type Err = InvalidNotificationType;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "email" => Ok(NotificationType::EMAIL),
            "sms" => Ok(NotificationType::SMS),
            _ => Err(InvalidNotificationType),
        }
    }
}

impl std::fmt::Display for NotificationType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationType::EMAIL => write!(f, "email"),
            NotificationType::SMS => write!(f, "sms"),
        }
    }
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum NotificationStatus {
    CREATED,
    SENT,
    FAILURE,
    SUCCESS,
}

impl std::str::FromStr for NotificationStatus {
    type Err = InvalidNotificationStatus;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "created" => Ok(NotificationStatus::CREATED),
            "sent" => Ok(NotificationStatus::SENT),
            "failure" => Ok(NotificationStatus::FAILURE),
            "success" => Ok(NotificationStatus::SUCCESS),
            _ => Err(InvalidNotificationStatus),
        }
    }
}

impl std::fmt::Display for NotificationStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationStatus::CREATED => write!(f, "created"),
            NotificationStatus::SENT => write!(f, "sent"),
            NotificationStatus::FAILURE => write!(f, "failure"),
            NotificationStatus::SUCCESS => write!(f, "success"),
        }
    }
}

#[allow(non_camel_case_types)]
#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum NotificationTemplate {
    LABOUR_UPDATE,
    LABOUR_INVITE,
    SUBSCRIBER_INVITE,
    CONTACT_US_SUBMISSION,
}

impl std::str::FromStr for NotificationTemplate {
    type Err = InvalidNotificationTemplate;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "labour_update" => Ok(NotificationTemplate::LABOUR_UPDATE),
            "labour_invite" => Ok(NotificationTemplate::LABOUR_INVITE),
            "subscriber_invite" => Ok(NotificationTemplate::SUBSCRIBER_INVITE),
            "contact_us_submission" => Ok(NotificationTemplate::CONTACT_US_SUBMISSION),
            _ => Err(InvalidNotificationTemplate),
        }
    }
}

impl std::fmt::Display for NotificationTemplate {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationTemplate::LABOUR_UPDATE => write!(f, "labour_update"),
            NotificationTemplate::LABOUR_INVITE => write!(f, "labour_invite"),
            NotificationTemplate::SUBSCRIBER_INVITE => write!(f, "subscriber_invite"),
            NotificationTemplate::CONTACT_US_SUBMISSION => write!(f, "contact_us_submission"),
        }
    }
}