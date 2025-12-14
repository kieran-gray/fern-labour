use async_trait::async_trait;
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

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct User {
    pub user_id: String,
    pub issuer: String,
    pub email: Option<String>,
    pub email_verified: Option<bool>,
    pub name: Option<String>,
}

#[derive(Deserialize)]
struct AuthenticateResponse {
    user: User,
}

#[derive(Deserialize)]
struct ErrorResponse {
    message: String,
}

#[async_trait(?Send)]
pub trait AuthServiceClient {
    async fn verify_token(&self, token: &str) -> Result<String, AuthClientError>;
    async fn authenticate(&self, token: &str) -> Result<User, AuthClientError>;
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
        let mut response = self
            .fetcher
            .fetch("https://quest-lock.com/api/v1/auth/verify/", Some(init))
            .await
            .map_err(|e| {
                error!(error = ?e, "Auth service request failed");
                AuthClientError::RequestFailed(format!("Auth service request failed: {e}"))
            })?;

        match response.status_code() {
            200 => {
                let verify_response: VerifyTokenResponse = response.json().await.map_err(|e| {
                    error!(error = ?e, "Failed to parse verify response");
                    AuthClientError::ParseError(format!("Failed to parse verify response: {e}"))
                })?;

                debug!(user_id = %verify_response.user_id, "Token verified via auth service");
                Ok(verify_response.user_id)
            }
            401 => {
                let error_response: ErrorResponse =
                    response.json().await.unwrap_or_else(|_| ErrorResponse {
                        message: "Unauthorised".to_string(),
                    });
                Err(AuthClientError::Unauthorised(error_response.message))
            }
            status => {
                let error_response: ErrorResponse =
                    response.json().await.unwrap_or_else(|_| ErrorResponse {
                        message: format!("Unexpected status: {}", status),
                    });
                Err(AuthClientError::RequestFailed(error_response.message))
            }
        }
    }

    async fn authenticate(&self, token: &str) -> Result<User, AuthClientError> {
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

        let mut response = self
            .fetcher
            .fetch(
                "https://quest-lock.com/api/v1/auth/authenticate/",
                Some(init),
            )
            .await
            .map_err(|e| {
                error!(error = ?e, "Auth service authenticate request failed");
                AuthClientError::RequestFailed(format!("Auth service request failed: {e}"))
            })?;

        match response.status_code() {
            200 => {
                let auth_response: AuthenticateResponse = response.json().await.map_err(|e| {
                    error!(error = ?e, "Failed to parse authenticate response");
                    AuthClientError::ParseError(format!(
                        "Failed to parse authenticate response: {e}"
                    ))
                })?;

                debug!(
                    user_id = %auth_response.user.user_id,
                    issuer = %auth_response.user.issuer,
                    "Token authenticated via auth service"
                );
                Ok(auth_response.user)
            }
            401 => {
                let error_response: ErrorResponse =
                    response.json().await.unwrap_or_else(|_| ErrorResponse {
                        message: "Unauthorised".to_string(),
                    });
                Err(AuthClientError::Unauthorised(error_response.message))
            }
            status => {
                let error_response: ErrorResponse =
                    response.json().await.unwrap_or_else(|_| ErrorResponse {
                        message: format!("Unexpected status: {}", status),
                    });
                Err(AuthClientError::RequestFailed(error_response.message))
            }
        }
    }
}
