#[derive(Debug, Clone)]
pub enum NotificationError {
    AlreadyExists,
    NotFound,
    InvalidStateTransition(String),
    ValidationError(String),
    MissingExternalId,
    InvalidCommand(String),
}

impl std::fmt::Display for NotificationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationError::AlreadyExists => write!(f, "Notification already exists"),
            NotificationError::NotFound => write!(f, "Notification not found"),
            NotificationError::InvalidStateTransition(msg) => {
                write!(f, "Invalid state transition: {msg}")
            }
            NotificationError::ValidationError(msg) => write!(f, "Validation error: {msg}"),
            NotificationError::MissingExternalId => {
                write!(f, "Missing external ID")
            }
            NotificationError::InvalidCommand(msg) => write!(f, "Invalid command: {msg}"),
        }
    }
}

impl std::error::Error for NotificationError {}
