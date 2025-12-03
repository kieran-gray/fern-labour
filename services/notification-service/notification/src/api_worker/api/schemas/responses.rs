use serde_json::json;

use crate::api_worker::api::exceptions::ApiError;

const HTTP_STATUS_BAD_REQUEST: u16 = 400;
const HTTP_STATUS_UNAUTHORISED: u16 = 401;
const HTTP_STATUS_NOT_FOUND: u16 = 404;
const HTTP_STATUS_INTERNAL_SERVER_ERROR: u16 = 500;

impl From<ApiError> for worker::Response {
    fn from(error: ApiError) -> Self {
        let (status, message) = match &error {
            ApiError::NotFound(msg) => (HTTP_STATUS_NOT_FOUND, msg.as_str()),
            ApiError::Unauthorised(msg) => (HTTP_STATUS_UNAUTHORISED, msg.as_str()),
            ApiError::ValidationError(msg) => (HTTP_STATUS_BAD_REQUEST, msg.as_str()),
            ApiError::InternalServerError(msg) => (HTTP_STATUS_INTERNAL_SERVER_ERROR, msg.as_str()),
        };

        let body = json!({ "message": message });
        worker::Response::from_json(&body)
            .unwrap()
            .with_status(status)
    }
}
