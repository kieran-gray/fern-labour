use std::fmt;

#[derive(Debug, Clone)]
pub struct InvalidNotificationType;

impl fmt::Display for InvalidNotificationType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Invalid NotificationType provided.")
    }
}

#[derive(Debug, Clone)]
pub struct InvalidNotificationStatus;

impl fmt::Display for InvalidNotificationStatus {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Invalid NotificationStatus provided.")
    }
}

#[derive(Debug, Clone)]
pub struct InvalidNotificationTemplate;

impl fmt::Display for InvalidNotificationTemplate {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Invalid NotificationTemplate provided.")
    }
}
