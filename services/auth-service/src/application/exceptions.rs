use crate::domain::exceptions::DomainError;

#[derive(Debug)]
pub enum AppError {
    DatabaseError(String),
    NotFound(String),
    Unauthorised(String),
    InternalError(String),
    ValidationError(String),
    TokenVerificationError(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AppError::DatabaseError(msg) => write!(f, "Database error: {msg}"),
            AppError::NotFound(msg) => write!(f, "Not found: {msg}"),
            AppError::Unauthorised(msg) => write!(f, "Unauthorised: {msg}"),
            AppError::InternalError(msg) => write!(f, "Internal server error: {msg}"),
            AppError::ValidationError(msg) => write!(f, "Validation error: {msg}"),
            AppError::TokenVerificationError(msg) => write!(f, "Token verification error: {msg}"),
        }
    }
}

impl From<DomainError> for AppError {
    fn from(value: DomainError) -> Self {
        AppError::ValidationError(value.to_string())
    }
}

impl std::error::Error for AppError {}

#[derive(Debug)]
pub enum AuthError {
    InvalidToken(String),
    Unauthorised(String),
    InternalError(String),
    ValidationFailed,
    ExtractionFailed,
}

impl std::fmt::Display for AuthError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AuthError::InvalidToken(msg) => write!(f, "Invalid token: {msg}"),
            AuthError::Unauthorised(msg) => write!(f, "Unauthorised: {msg}"),
            AuthError::InternalError(msg) => write!(f, "Internal error: {msg}"),
            AuthError::ValidationFailed => write!(f, "Token Validation Failed"),
            AuthError::ExtractionFailed => write!(f, "Token Extraction Failed"),
        }
    }
}
