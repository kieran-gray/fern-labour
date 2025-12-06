#[derive(Debug)]
pub enum DispatchClientError {
    SerializationError(String),
    RequestFailed(String),
    InternalError(String),
}

impl std::fmt::Display for DispatchClientError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DispatchClientError::SerializationError(e) => write!(f, "Serialization error: {}", e),
            DispatchClientError::RequestFailed(e) => write!(f, "Request failed: {}", e),
            DispatchClientError::InternalError(e) => write!(f, "Internal error: {}", e),
        }
    }
}

impl std::error::Error for DispatchClientError {}

#[derive(Debug)]
pub enum WebhookForwardError {
    RequestFailed(String),
    InvalidResponse(String),
    Unauthorized,
    ServerError(String),
}

impl std::fmt::Display for WebhookForwardError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            WebhookForwardError::RequestFailed(e) => write!(f, "Request failed: {}", e),
            WebhookForwardError::InvalidResponse(e) => write!(f, "Invalid response: {}", e),
            WebhookForwardError::Unauthorized => write!(f, "Webhook verification failed"),
            WebhookForwardError::ServerError(e) => write!(f, "Server error: {}", e),
        }
    }
}

impl std::error::Error for WebhookForwardError {}
