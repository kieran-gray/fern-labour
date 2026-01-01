use anyhow::{Context, Result, anyhow};
use async_trait::async_trait;
use chrono::Utc;
use fern_labour_notifications_shared::value_objects::NotificationChannel;
use serde::Serialize;
use tracing::{error, info};

use super::aws_sigv4::AwsSigV4Signer;
use crate::{
    application::dispatch::{DispatchContext, NotificationGatewayTrait},
    setup::config::SesConfig,
};

pub struct SesEmailNotificationGateway {
    signer: AwsSigV4Signer,
    host: String,
    from_email: String,
    from_name: String,
}

impl SesEmailNotificationGateway {
    pub fn create(config: &SesConfig) -> Self {
        let host = format!("email.{}.amazonaws.com", config.region);
        let signer = AwsSigV4Signer::new(
            config.access_key_id.clone(),
            config.secret_access_key.clone(),
            config.region.clone(),
            "ses".to_string(),
        );

        Self {
            signer,
            host,
            from_email: config.from_email.clone(),
            from_name: config.from_name.clone(),
        }
    }
}

#[derive(Serialize)]
#[serde(rename_all = "PascalCase")]
struct SendEmailRequest {
    from_email_address: String,
    destination: Destination,
    content: Content,
}

#[derive(Serialize)]
#[serde(rename_all = "PascalCase")]
struct Destination {
    to_addresses: Vec<String>,
}

#[derive(Serialize)]
#[serde(rename_all = "PascalCase")]
struct Content {
    simple: SimpleContent,
}

#[derive(Serialize)]
#[serde(rename_all = "PascalCase")]
struct SimpleContent {
    subject: MessageContent,
    body: Body,
}

#[derive(Serialize)]
#[serde(rename_all = "PascalCase")]
struct MessageContent {
    data: String,
    charset: String,
}

#[derive(Serialize)]
#[serde(rename_all = "PascalCase")]
struct Body {
    html: MessageContent,
}

#[async_trait(?Send)]
impl NotificationGatewayTrait for SesEmailNotificationGateway {
    fn channel(&self) -> NotificationChannel {
        NotificationChannel::EMAIL
    }

    fn provider(&self) -> &str {
        "ses"
    }

    async fn dispatch(&self, context: &DispatchContext) -> Result<Option<String>> {
        let from = format!("{} <{}>", self.from_name, self.from_email);
        let subject = context
            .content
            .subject()
            .ok_or_else(|| anyhow!("Email subject is required"))?;

        let request_body = SendEmailRequest {
            from_email_address: from,
            destination: Destination {
                to_addresses: vec![context.destination.as_str().to_string()],
            },
            content: Content {
                simple: SimpleContent {
                    subject: MessageContent {
                        data: subject.to_string(),
                        charset: "UTF-8".to_string(),
                    },
                    body: Body {
                        html: MessageContent {
                            data: context.content.body().to_string(),
                            charset: "UTF-8".to_string(),
                        },
                    },
                },
            },
        };

        let payload =
            serde_json::to_string(&request_body).context("Failed to serialize email request")?;

        let path = "/v2/email/outbound-emails";
        let url = format!("https://{}{}", self.host, path);

        let content_type_header = ("content-type".to_string(), "application/json".to_string());
        let signed_headers = self.signer.sign_request(
            "POST",
            &self.host,
            path,
            &[content_type_header],
            &payload,
            Utc::now(),
        );

        let mut request_init = worker::RequestInit::new();
        request_init.with_method(worker::Method::Post);

        let headers = worker::Headers::new();
        headers
            .set("Content-Type", "application/json")
            .context("Failed to set Content-Type header")?;
        headers
            .set("Authorization", &signed_headers.authorization)
            .context("Failed to set Authorization header")?;
        headers
            .set("X-Amz-Date", &signed_headers.x_amz_date)
            .context("Failed to set X-Amz-Date header")?;
        headers
            .set("X-Amz-Content-Sha256", &signed_headers.x_amz_content_sha256)
            .context("Failed to set X-Amz-Content-Sha256 header")?;

        request_init.with_headers(headers);
        request_init.with_body(Some(payload.into()));

        let mut response =
            worker::Fetch::Request(worker::Request::new_with_init(&url, &request_init)?)
                .send()
                .await
                .map_err(|e| anyhow!("SES API request failed: {e}"))?;

        let status = response.status_code();
        if !(200..=299).contains(&status) {
            let error_text = response
                .text()
                .await
                .context("Failed to read error response")?;

            error!(
                notification_id = %context.notification_id,
                status = status,
                error = %error_text,
                "SES API error"
            );
            return Err(anyhow!("SES API error (status {}): {}", status, error_text));
        }

        let response_json: serde_json::Value = response
            .json()
            .await
            .map_err(|e| anyhow!("Failed to parse SES response: {e}"))?;

        let message_id = response_json["MessageId"]
            .as_str()
            .ok_or_else(|| anyhow!("No 'MessageId' field in SES response"))?
            .to_string();

        info!(
            notification_id = %context.notification_id,
            message_id = %message_id,
            "Successfully sent email via SES"
        );

        Ok(Some(message_id))
    }
}
