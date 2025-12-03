use anyhow::{Result, anyhow};
use async_trait::async_trait;
use fern_labour_notifications_shared::value_objects::NotificationChannel;
use resend_rs::{Resend, types::CreateEmailBaseOptions};
use tracing::{error, info};

use crate::{
    application::dispatch::{DispatchContext, NotificationGatewayTrait},
    setup::config::ResendConfig,
};

pub struct ResendEmailNotificationGateway {
    pub config: ResendConfig,
}

impl ResendEmailNotificationGateway {
    pub fn create(config: &ResendConfig) -> Self {
        Self {
            config: config.clone(),
        }
    }
}

#[async_trait(?Send)]
impl NotificationGatewayTrait for ResendEmailNotificationGateway {
    fn channel(&self) -> NotificationChannel {
        NotificationChannel::EMAIL
    }

    fn provider(&self) -> &str {
        "resend"
    }

    async fn dispatch(&self, context: &DispatchContext) -> Result<Option<String>> {
        let resend = Resend::new(&self.config.api_key);
        let from = format!("{} <{}>", self.config.from_name, self.config.from_email);

        let email = CreateEmailBaseOptions::new(
            from,
            [context.destination.as_str()],
            context.content.subject().unwrap(),
        )
        .with_html(context.content.body())
        .with_idempotency_key(&context.idempotency_key);

        match resend.emails.send(email).await {
            Ok(response) => {
                info!(
                    notification_id = %context.notification_id,
                    external_id = %response.id,
                    "Email sent successfully via Resend"
                );
                Ok(Some(response.id.to_string()))
            }
            Err(err) => {
                error!(
                    notification_id = %context.notification_id,
                    error = %err,
                    "Failed to send email via Resend"
                );
                Err(anyhow!(err))
            }
        }
    }
}
