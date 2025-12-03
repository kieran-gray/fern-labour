use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use tracing::{debug, error};
use worker::{Fetcher, Headers, Method, RequestInit};

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

#[async_trait(?Send)]
pub trait AuthServiceClient {
    async fn verify_token(&self, token: &str) -> Result<String, AuthClientError>;
}

pub struct FetcherAuthServiceClient {
    fetcher: Fetcher,
}

impl FetcherAuthServiceClient {
    pub fn create(fetcher: Fetcher) -> Self {
        Self { fetcher }
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

        // The 'https://fern-labour.com' bit of the URL below does nothing since we are calling the
        // service directly. It is required to be a valid URL though.
        let mut response = self
            .fetcher
            .fetch("https://fern-labour.com/api/v1/auth/verify/", Some(init))
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
            401 => Err(AuthClientError::Unauthorised("Unauthorised".to_string())),
            code => Err(AuthClientError::RequestFailed(format!(
                "Unexpected status: {code}"
            ))),
        }
    }
}
