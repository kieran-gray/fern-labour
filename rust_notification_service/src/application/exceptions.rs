use sqlx::Error as SqlxError;
use thiserror::Error;
use tracing::error;

/// AppError is an enum that represents various types of errors that can occur in the application.
/// It implements the `std::error::Error` trait and the `axum::response::IntoResponse` trait.
#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    DatabaseError(#[from] SqlxError),
    #[error("Not found: {0}")]
    NotFound(String),
    #[error("Internal server error")]
    InternalError,
    #[error("Validation error: {0}")]
    ValidationError(String),
    #[error("Invalid Subscription: {0}")]
    InvalidSubscription(String),
    #[error("Invalid Event Body: {0}")]
    InvalidEventBody(String),

    /// Used for authentication-related errors
    #[error("Wrong credentials")]
    WrongCredentials,
    #[error("Missing credentials")]
    MissingCredentials,
    #[error("Invalid token")]
    InvalidToken,
    #[error("Token creation error")]
    TokenCreation,
    #[error("User not found")]
    UserNotFound,
}
