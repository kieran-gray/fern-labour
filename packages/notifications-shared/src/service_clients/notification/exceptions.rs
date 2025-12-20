#[derive(Debug)]
pub enum NotificationClientError {
    SerializationError(String),
    RequestFailed(String),
    InternalError(String),
}

impl std::fmt::Display for NotificationClientError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NotificationClientError::SerializationError(e) => {
                write!(f, "Serialization error: {}", e)
            }
            NotificationClientError::RequestFailed(e) => write!(f, "Request failed: {}", e),
            NotificationClientError::InternalError(e) => write!(f, "Internal error: {}", e),
        }
    }
}

impl std::error::Error for NotificationClientError {}
