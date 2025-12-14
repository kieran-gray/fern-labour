use chrono::Utc;
use fern_labour_event_sourcing_rs::{CommandEnvelope, CommandMetadata};
use serde::Serialize;
use tracing::error;
use uuid::Uuid;
use worker::{Headers, Method, ObjectNamespace, Request, RequestInit, Response};

use crate::clients::worker_clients::auth::User;

#[derive(Debug)]
pub enum DurableObjectCQRSClientError {
    StubError(String),
    SerializationError(String),
    RequestError(String),
    DurableObjectError(String),
}

impl std::fmt::Display for DurableObjectCQRSClientError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DurableObjectCQRSClientError::StubError(msg) => {
                write!(f, "Failed to get DO stub: {msg}")
            }
            DurableObjectCQRSClientError::SerializationError(msg) => {
                write!(f, "Serialization error: {msg}")
            }
            DurableObjectCQRSClientError::RequestError(msg) => {
                write!(f, "Request error: {msg}")
            }
            DurableObjectCQRSClientError::DurableObjectError(msg) => {
                write!(f, "Durable Object error: {msg}")
            }
        }
    }
}

impl std::error::Error for DurableObjectCQRSClientError {}

pub struct DurableObjectCQRSClient {
    namespace: ObjectNamespace,
}

impl DurableObjectCQRSClient {
    pub fn create(namespace: ObjectNamespace) -> Self {
        Self { namespace }
    }

    fn create_headers_with_user(user: &User) -> Result<Headers, DurableObjectCQRSClientError> {
        let headers = Headers::new();

        let user_json = serde_json::to_string(user).map_err(|e| {
            DurableObjectCQRSClientError::SerializationError(format!(
                "Failed to serialize user: {}",
                e
            ))
        })?;

        headers
            .set("X-User-Info", &user_json)
            .map_err(|e| {
                DurableObjectCQRSClientError::RequestError(format!(
                    "Failed to set X-User-Info header: {}",
                    e
                ))
            })?;

        headers
            .set("Content-Type", "application/json")
            .map_err(|e| {
                DurableObjectCQRSClientError::RequestError(format!(
                    "Failed to set Content-Type header: {}",
                    e
                ))
            })?;

        Ok(headers)
    }

    pub async fn command<C: Serialize>(
        &self,
        aggregate_id: Uuid,
        command: C,
        user: &User,
        url: &str,
    ) -> Result<Response, DurableObjectCQRSClientError> {
        let aggregate_stub = self
            .namespace
            .get_by_name(&aggregate_id.to_string())
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "Failed to get DO stub");
                DurableObjectCQRSClientError::StubError(format!(
                    "Could not fetch aggregate stub: {e}"
                ))
            })?;

        let correlation_id = Uuid::now_v7();
        let metadata = CommandMetadata::new(
            aggregate_id,
            correlation_id,
            correlation_id,
            user.user_id.clone(),
            Utc::now(),
        );

        let command_envelope = CommandEnvelope::new(metadata, command);

        let body_string = serde_json::to_string(&command_envelope).map_err(|e| {
            error!(error = ?e, "Failed to serialize command envelope");
            DurableObjectCQRSClientError::SerializationError(format!(
                "Failed to serialize request body: {e}"
            ))
        })?;

        let headers = Self::create_headers_with_user(user)?;

        let mut init = RequestInit::new();
        init.with_method(Method::Post);
        init.with_headers(headers);
        init.with_body(Some(body_string.into()));

        let request =
            Request::new_with_init(&format!("https://durable.fern-labour.com{url}"), &init)
                .map_err(|e| {
                    error!(error = ?e, "Failed to create request");
                    DurableObjectCQRSClientError::RequestError(format!(
                        "Failed to create request: {e}"
                    ))
                })?;

        let response = aggregate_stub
            .fetch_with_request(request)
            .await
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "DO fetch failed");
                DurableObjectCQRSClientError::DurableObjectError(format!(
                    "Durable Object responded with error: {e}"
                ))
            })?;

        Ok(response)
    }

    pub async fn send_envelope<C: Serialize>(
        &self,
        aggregate_id: Uuid,
        url: &str,
        envelope: CommandEnvelope<C>,
        user: &User,
    ) -> Result<Response, DurableObjectCQRSClientError> {
        let aggregate_stub = self
            .namespace
            .get_by_name(&aggregate_id.to_string())
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "Failed to get DO stub");
                DurableObjectCQRSClientError::StubError(format!(
                    "Could not fetch aggregate stub: {e}"
                ))
            })?;

        let body_string = serde_json::to_string(&envelope).map_err(|e| {
            error!(error = ?e, "Failed to serialize command envelope");
            DurableObjectCQRSClientError::SerializationError(format!(
                "Failed to serialize request body: {e}"
            ))
        })?;

        let headers = Self::create_headers_with_user(user)?;

        let mut init = RequestInit::new();
        init.with_method(Method::Post);
        init.with_headers(headers);
        init.with_body(Some(body_string.into()));

        let request =
            Request::new_with_init(&format!("https://durable.fern-labour.com{url}"), &init)
                .map_err(|e| {
                    error!(error = ?e, "Failed to create request");
                    DurableObjectCQRSClientError::RequestError(format!(
                        "Failed to create request: {e}"
                    ))
                })?;

        let response = aggregate_stub
            .fetch_with_request(request)
            .await
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "DO fetch failed");
                DurableObjectCQRSClientError::DurableObjectError(format!(
                    "Durable Object responded with error: {e}"
                ))
            })?;

        Ok(response)
    }

    pub async fn query(
        &self,
        aggregate_id: Uuid,
        url: &str,
        user: &User,
    ) -> Result<Response, DurableObjectCQRSClientError> {
        let aggregate_stub = self
            .namespace
            .get_by_name(&aggregate_id.to_string())
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "Failed to get DO stub");
                DurableObjectCQRSClientError::StubError(format!(
                    "Could not fetch aggregate stub: {e}"
                ))
            })?;

        let headers = Self::create_headers_with_user(user)?;

        let mut init = RequestInit::new();
        init.with_method(Method::Get);
        init.with_headers(headers);

        let request =
            Request::new_with_init(&format!("https://durable.fern-labour.com{url}"), &init)
                .map_err(|e| {
                    error!(error = ?e, "Failed to create request");
                    DurableObjectCQRSClientError::RequestError(format!(
                        "Failed to create request: {e}"
                    ))
                })?;

        let response = aggregate_stub
            .fetch_with_request(request)
            .await
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "DO query failed");
                DurableObjectCQRSClientError::DurableObjectError(format!(
                    "Durable Object responded with error: {e}"
                ))
            })?;

        Ok(response)
    }

    pub async fn query_with_body<Q: Serialize>(
        &self,
        aggregate_id: Uuid,
        query: Q,
        user: &User,
        url: &str,
    ) -> Result<Response, DurableObjectCQRSClientError> {
        let aggregate_stub = self
            .namespace
            .get_by_name(&aggregate_id.to_string())
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "Failed to get DO stub");
                DurableObjectCQRSClientError::StubError(format!(
                    "Could not fetch aggregate stub: {e}"
                ))
            })?;

        let body_string = serde_json::to_string(&query).map_err(|e| {
            error!(error = ?e, "Failed to serialize query");
            DurableObjectCQRSClientError::SerializationError(format!(
                "Failed to serialize request body: {e}"
            ))
        })?;

        let headers = Self::create_headers_with_user(user)?;

        let mut init = RequestInit::new();
        init.with_method(Method::Post);
        init.with_headers(headers);
        init.with_body(Some(body_string.into()));

        let request =
            Request::new_with_init(&format!("https://durable.fern-labour.com{url}"), &init)
                .map_err(|e| {
                    error!(error = ?e, "Failed to create request");
                    DurableObjectCQRSClientError::RequestError(format!(
                        "Failed to create request: {e}"
                    ))
                })?;

        let response = aggregate_stub
            .fetch_with_request(request)
            .await
            .map_err(|e| {
                error!(error = ?e, aggregate_id = %aggregate_id, "DO query failed");
                DurableObjectCQRSClientError::DurableObjectError(format!(
                    "Durable Object responded with error: {e}"
                ))
            })?;

        Ok(response)
    }
}
