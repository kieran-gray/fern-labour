use axum::{
    BoxError,
    http::StatusCode,
    response::{IntoResponse, Response},
};

use tracing::error;

use crate::application::exceptions::AppError;

use super::schemas::responses::{ApiResponse, RestApiResponse};

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let status = match self {
            AppError::ValidationError(_) => StatusCode::BAD_REQUEST,
            AppError::DatabaseError(_) => StatusCode::INTERNAL_SERVER_ERROR,
            AppError::NotFound(_) => StatusCode::NOT_FOUND,
            AppError::InvalidSubscription(_) => StatusCode::BAD_REQUEST,
            AppError::InvalidEventBody(_) => StatusCode::BAD_REQUEST,
            AppError::InternalError => StatusCode::INTERNAL_SERVER_ERROR,
            AppError::WrongCredentials => StatusCode::UNAUTHORIZED,
            AppError::MissingCredentials => StatusCode::BAD_REQUEST,
            AppError::InvalidToken => StatusCode::UNAUTHORIZED,
            AppError::TokenCreation => StatusCode::INTERNAL_SERVER_ERROR,
            AppError::UserNotFound => StatusCode::NOT_FOUND,
        };
        let body = axum::Json(ApiResponse::<()> {
            status: status.as_u16(),
            message: self.to_string(),
            data: None,
        });

        (status, body).into_response()
    }
}

pub async fn handle_error(error: BoxError) -> impl IntoResponse {
    let status = if error.is::<tower::timeout::error::Elapsed>() {
        StatusCode::REQUEST_TIMEOUT
    } else {
        StatusCode::INTERNAL_SERVER_ERROR
    };

    let message = error.to_string();
    error!(?status, %message, "Request failed");

    let body = RestApiResponse::<()>::failure(status.as_u16(), message);

    (status, body)
}
