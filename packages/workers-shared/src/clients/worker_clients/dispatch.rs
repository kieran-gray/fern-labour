use async_trait::async_trait;
use fern_labour_notifications_shared::service_clients::{
    DispatchClient, DispatchClientError, DispatchRequest, DispatchResponse,
};
use tracing::{debug, error};
use worker::{Headers, Method, RequestInit, Response};

pub struct FetcherDispatchClient {
    fetcher: worker::Fetcher,
}

impl FetcherDispatchClient {
    pub fn create(fetcher: worker::Fetcher) -> Self {
        Self { fetcher }
    }

    async fn do_dispatch(
        &self,
        request: DispatchRequest,
        url: &str,
    ) -> Result<Response, DispatchClientError> {
        let body_bytes = serde_json::to_vec(&request).map_err(|e| {
            DispatchClientError::SerializationError(format!("Failed to serialize request: {e}"))
        })?;

        let headers = vec![
            ("Content-Type", "application/json"),
            ("X-Service-ID", "notification-service"),
        ];

        let worker_headers = Headers::new();
        for (name, value) in headers {
            worker_headers.set(name, value).map_err(|e| {
                DispatchClientError::InternalError(format!("Failed to set header {}: {}", name, e))
            })?;
        }

        let mut init = RequestInit::new();
        init.with_method(Method::Post);
        init.with_headers(worker_headers);
        init.with_body(Some(body_bytes.into()));

        self.fetcher.fetch(url, Some(init)).await.map_err(|e| {
            error!(error = ?e, "Dispatch service request failed");
            DispatchClientError::RequestFailed(format!("Request failed: {e}"))
        })
    }
}

#[async_trait(?Send)]
impl DispatchClient for FetcherDispatchClient {
    async fn dispatch_async(
        &self,
        request: DispatchRequest,
    ) -> Result<Response, DispatchClientError> {
        self.do_dispatch(request, "https://fernlabour.com/api/v1/dispatch-async")
            .await
    }

    async fn dispatch(
        &self,
        request: DispatchRequest,
    ) -> Result<Option<String>, DispatchClientError> {
        let mut response = self
            .do_dispatch(request, "https://fernlabour.com/api/v1/dispatch")
            .await?;
        match response.status_code() {
            200..=202 => {
                debug!("Notification dispatched successfully");
                let dispatch_response: DispatchResponse = response.json().await.map_err(|e| {
                    DispatchClientError::InternalError(format!("Failed to parse response: {e}"))
                })?;
                Ok(dispatch_response.external_id)
            }
            400..=499 => Err(DispatchClientError::RequestFailed(format!(
                "Client error: {}",
                response.status_code()
            ))),
            500..=599 => Err(DispatchClientError::InternalError(format!(
                "Server error: {}",
                response.status_code()
            ))),
            code => Err(DispatchClientError::RequestFailed(format!(
                "Unexpected status: {code}"
            ))),
        }
    }
}
