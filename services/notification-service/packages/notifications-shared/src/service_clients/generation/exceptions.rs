#[derive(Debug)]
pub enum GenerationClientError {
    SerializationError(String),
    RequestFailed(String),
    InternalError(String),
}

impl std::fmt::Display for GenerationClientError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            GenerationClientError::SerializationError(e) => {
                write!(f, "Serialization error: {}", e)
            }
            GenerationClientError::RequestFailed(e) => write!(f, "Request failed: {}", e),
            GenerationClientError::InternalError(e) => write!(f, "Internal error: {}", e),
        }
    }
}

impl std::error::Error for GenerationClientError {}
