use async_trait::async_trait;
use fern_labour_notifications_shared::service_clients::{
    GenerationClient, GenerationClientError, RenderRequest, RenderResponse,
};
use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationTemplateData, RenderedContent,
};
use tracing::{debug, error};
use uuid::Uuid;
use worker::{Headers, Method, RequestInit, Response};

pub struct FetcherGenerationClient {
    fetcher: worker::Fetcher,
}

impl FetcherGenerationClient {
    pub fn create(fetcher: worker::Fetcher) -> Self {
        Self { fetcher }
    }

    async fn do_render(
        &self,
        notification_id: Uuid,
        channel: NotificationChannel,
        template_data: NotificationTemplateData,
        url: &str,
    ) -> Result<Response, GenerationClientError> {
        let request = RenderRequest {
            notification_id,
            channel,
            template_data,
        };

        let body_bytes = serde_json::to_vec(&request).map_err(|e| {
            GenerationClientError::SerializationError(format!("Failed to serialize request: {e}"))
        })?;

        let headers = vec![
            ("Content-Type", "application/json"),
            ("X-Service-ID", "notification-service"),
        ];

        let worker_headers = Headers::new();
        for (name, value) in headers {
            worker_headers.set(name, value).map_err(|e| {
                GenerationClientError::InternalError(format!(
                    "Failed to set header {}: {}",
                    name, e
                ))
            })?;
        }

        let mut init = RequestInit::new();
        init.with_method(Method::Post);
        init.with_headers(worker_headers);
        init.with_body(Some(body_bytes.into()));

        self.fetcher.fetch(url, Some(init)).await.map_err(|e| {
            error!(error = ?e, "Generation service request failed");
            GenerationClientError::RequestFailed(format!("Request failed: {e}"))
        })
    }
}

#[async_trait(?Send)]
impl GenerationClient for FetcherGenerationClient {
    async fn render_async(
        &self,
        notification_id: Uuid,
        channel: NotificationChannel,
        template_data: NotificationTemplateData,
    ) -> Result<Response, GenerationClientError> {
        self.do_render(
            notification_id,
            channel,
            template_data,
            "https://fern-labour.com/api/v1/render-async",
        )
        .await
    }

    async fn render(
        &self,
        notification_id: Uuid,
        channel: NotificationChannel,
        template_data: NotificationTemplateData,
    ) -> Result<RenderedContent, GenerationClientError> {
        let mut response = self
            .do_render(
                notification_id,
                channel,
                template_data,
                "https://fern-labour.com/api/v1/render",
            )
            .await?;
        match response.status_code() {
            200..=202 => {
                debug!("Template rendered successfully");
                let render_response: RenderResponse = response.json().await.map_err(|e| {
                    GenerationClientError::InternalError(format!("Failed to parse response: {e}"))
                })?;
                Ok(render_response.rendered_content)
            }
            400..=499 => Err(GenerationClientError::RequestFailed(format!(
                "Client error: {}",
                response.status_code()
            ))),
            500..=599 => Err(GenerationClientError::InternalError(format!(
                "Server error: {}",
                response.status_code()
            ))),
            code => Err(GenerationClientError::RequestFailed(format!(
                "Unexpected status: {code}"
            ))),
        }
    }
}
