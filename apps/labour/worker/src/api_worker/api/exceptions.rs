#[derive(Debug)]
pub enum ApiError {
    NotFound(String),
    Unauthorised(String),
    ValidationError(String),
    InternalServerError(String),
}

impl std::fmt::Display for ApiError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ApiError::NotFound(msg) => write!(f, "Not found: {msg}"),
            ApiError::Unauthorised(msg) => write!(f, "Unauthorised: {msg}"),
            ApiError::ValidationError(msg) => write!(f, "Validation error: {msg}"),
            ApiError::InternalServerError(msg) => write!(f, "Internal server error: {msg}"),
        }
    }
}

impl std::error::Error for ApiError {}
