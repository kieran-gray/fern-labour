use anyhow::{Result, anyhow};
use async_trait::async_trait;
use fern_labour_notifications_shared::value_objects::NotificationChannel;
use sendgrid::{Destination, Mail, SGClient};
use tracing::{error, info};

use crate::{
    application::dispatch::{DispatchContext, NotificationGatewayTrait},
    setup::config::SendgridConfig,
};

pub struct SendgridEmailNotificationGateway {
    pub config: SendgridConfig,
}

impl SendgridEmailNotificationGateway {
    pub fn create(config: &SendgridConfig) -> Self {
        Self {
            config: config.clone(),
        }
    }
}

#[async_trait(?Send)]
impl NotificationGatewayTrait for SendgridEmailNotificationGateway {
    fn channel(&self) -> NotificationChannel {
        NotificationChannel::EMAIL
    }

    fn provider(&self) -> &str {
        "sendgrid"
    }

    async fn dispatch(&self, context: &DispatchContext) -> Result<Option<String>> {
        let sg = SGClient::new(self.config.api_key.clone());

        let mail_info = Mail::new()
            .add_to(Destination {
                address: context.destination.as_str(),
                name: "",
            })
            .add_from(&self.config.from_email)
            .add_from_name(&self.config.from_name)
            .add_subject(context.content.subject().unwrap())
            .add_html(context.content.body());

        match sg.send(mail_info).await {
            Ok(_) => {
                info!(
                    notification_id = %context.notification_id,
                    "Email sent successfully via SendGrid"
                );
                Ok(None)
            }
            Err(err) => {
                error!(
                    notification_id = %context.notification_id,
                    error = %err,
                    "Failed to send email via SendGrid"
                );
                Err(anyhow!(err))
            }
        }
    }
}
