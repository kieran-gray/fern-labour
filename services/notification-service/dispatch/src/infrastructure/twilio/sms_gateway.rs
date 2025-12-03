use anyhow::{Context, Result, anyhow};
use async_trait::async_trait;
use base64::{Engine as _, engine::general_purpose};
use fern_labour_notifications_shared::value_objects::NotificationChannel;
use tracing::{error, info};

use crate::{
    application::dispatch::{DispatchContext, NotificationGatewayTrait},
    setup::config::TwilioConfig,
};

pub struct TwilioSmsNotificationGateway {
    twilio_url: String,
    twilio_auth: String,
    messaging_service_sid: String,
}

impl TwilioSmsNotificationGateway {
    pub fn create(twilio_config: &TwilioConfig) -> Self {
        let twilio_url = format!(
            "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json",
            twilio_config.account_sid
        );

        let credentials = format!("{}:{}", twilio_config.account_sid, twilio_config.auth_token);
        let twilio_auth = format!(
            "Basic {}",
            general_purpose::STANDARD.encode(credentials.as_bytes())
        );

        Self {
            twilio_url,
            twilio_auth,
            messaging_service_sid: twilio_config.messaging_service_sid.clone(),
        }
    }
}

#[async_trait(?Send)]
impl NotificationGatewayTrait for TwilioSmsNotificationGateway {
    fn channel(&self) -> NotificationChannel {
        NotificationChannel::SMS
    }

    fn provider(&self) -> &str {
        "twilio"
    }

    async fn dispatch(&self, context: &DispatchContext) -> Result<Option<String>> {
        let form_data = form_urlencoded::Serializer::new(String::new())
            .append_pair("To", context.destination.as_str())
            .append_pair("Body", context.content.body())
            .append_pair("MessagingServiceSid", &self.messaging_service_sid)
            .finish();

        let mut request_init = worker::RequestInit::new();
        request_init.with_method(worker::Method::Post);

        let headers = worker::Headers::new();
        headers
            .set("Authorization", &self.twilio_auth)
            .context("Failed to set Authorization header}")?;
        headers
            .set("Content-Type", "application/x-www-form-urlencoded")
            .context("Failed to set Content-Type header")?;

        request_init.with_headers(headers);
        request_init.with_body(Some(form_data.into()));

        let mut response = worker::Fetch::Request(worker::Request::new_with_init(
            &self.twilio_url,
            &request_init,
        )?)
        .send()
        .await
        .map_err(|e| anyhow!("Twilio API request failed: {e}"))?;

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
                "Twilio API error"
            );
            return Err(anyhow!(
                "Twilio API error (status {}): {}",
                status,
                error_text
            ));
        }

        let response_json: serde_json::Value = response
            .json()
            .await
            .map_err(|e| anyhow!("Failed to parse Twilio response: {e}"))?;

        let message_sid = response_json["sid"]
            .as_str()
            .ok_or_else(|| anyhow!("No 'sid' field in Twilio response"))?
            .to_string();

        info!(
            notification_id = %context.notification_id,
            message_sid = %message_sid,
            "Successfully sent SMS via Twilio"
        );
        Ok(Some(message_sid))
    }
}
