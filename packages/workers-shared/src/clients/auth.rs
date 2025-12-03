use async_trait::async_trait;
use http_body_util::BodyExt;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tracing::{debug, error};
use worker::{Headers, Method, RequestInit};

#[derive(Debug)]
pub enum AuthClientError {
    RequestFailed(String),
    ParseError(String),
    Unauthorised(String),
}

impl std::fmt::Display for AuthClientError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AuthClientError::RequestFailed(msg) => write!(f, "Request failed: {msg}"),
            AuthClientError::ParseError(msg) => write!(f, "Parse error: {msg}"),
            AuthClientError::Unauthorised(msg) => write!(f, "Unauthorised: {msg}"),
        }
    }
}

impl std::error::Error for AuthClientError {}

#[derive(Serialize)]
struct VerifyTokenRequest {
    token: String,
}

#[derive(Deserialize)]
struct VerifyTokenResponse {
    user_id: String,
}

#[derive(Deserialize)]
struct ErrorResponse {
    message: String,
}

#[async_trait(?Send)]
pub trait AuthServiceClient {
    async fn verify_token(&self, token: &str) -> Result<String, AuthClientError>;
}

pub struct FetcherAuthServiceClient {
    fetcher: Arc<worker::Fetcher>,
}

impl FetcherAuthServiceClient {
    pub fn create(fetcher: worker::Fetcher) -> Self {
        Self {
            fetcher: Arc::new(fetcher),
        }
    }
}

#[async_trait(?Send)]
impl AuthServiceClient for FetcherAuthServiceClient {
    async fn verify_token(&self, token: &str) -> Result<String, AuthClientError> {
        let body = VerifyTokenRequest {
            token: token.to_string(),
        };

        let body_bytes = serde_json::to_vec(&body).map_err(|e| {
            AuthClientError::ParseError(format!("Failed to serialize request: {e}"))
        })?;

        let headers = Headers::new();
        headers
            .set("Content-Type", "application/json")
            .map_err(|e| {
                AuthClientError::RequestFailed(format!("Failed to set Content-Type: {e}"))
            })?;

        let mut init = RequestInit::new();
        init.with_method(Method::Post);
        init.with_headers(headers);
        init.with_body(Some(body_bytes.into()));

        // The 'https://quest-lock.com' bit of the URL below does nothing since we are calling the
        // service directly. It is required to be a valid URL though.
        let response = self
            .fetcher
            .fetch("https://quest-lock.com/api/v1/auth/verify/", Some(init))
            .await
            .map_err(|e| {
                error!(error = ?e, "Auth service request failed");
                AuthClientError::RequestFailed(format!("Auth service request failed: {e}"))
            })?;

        let status = response.status();

        let body = response.into_body();

        let collected = body.collect().await.map_err(|e| {
            error!(error = ?e, "Failed to collect response body");
            AuthClientError::ParseError(format!("Failed to collect response body: {e}"))
        })?;

        let body_bytes = collected.to_bytes();

        if status == 200 {
            let verify_response: VerifyTokenResponse = serde_json::from_slice(&body_bytes)
                .map_err(|e| {
                    error!(error = ?e, "Failed to parse verify response");
                    AuthClientError::ParseError(format!("Failed to parse verify response: {e}"))
                })?;

            debug!(user_id = %verify_response.user_id, "Token verified via auth service");
            Ok(verify_response.user_id)
        } else if status == 401 {
            let error_response: ErrorResponse =
                serde_json::from_slice(&body_bytes).unwrap_or_else(|_| ErrorResponse {
                    message: "Unauthorised".to_string(),
                });
            Err(AuthClientError::Unauthorised(error_response.message))
        } else {
            let error_response: ErrorResponse =
                serde_json::from_slice(&body_bytes).unwrap_or_else(|_| ErrorResponse {
                    message: format!("Unexpected status: {}", status.as_u16()),
                });
            Err(AuthClientError::RequestFailed(error_response.message))
        }
    }
}
