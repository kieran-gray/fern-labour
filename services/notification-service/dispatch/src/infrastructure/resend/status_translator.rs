use anyhow::{Result, anyhow};
use fern_labour_notifications_shared::value_objects::NotificationStatus;

use crate::application::webhook::ProviderStatusTranslator;

pub struct ResendStatusTranslator;

impl ProviderStatusTranslator for ResendStatusTranslator {
    fn provider_name(&self) -> &str {
        "resend"
    }
    fn translate(&self, provider_event: &str) -> Result<NotificationStatus> {
        match provider_event {
            "email.sent" | "email.delivery_delayed" | "email.received" | "email.scheduled" => {
                Ok(NotificationStatus::SENT)
            }
            "email.delivered" | "email.complained" | "email.opened" | "email.clicked" => {
                Ok(NotificationStatus::DELIVERED)
            }
            "email.bounced" | "email.failed" => Ok(NotificationStatus::FAILED),
            _ => Err(anyhow!("Unknown resend event type: {}", provider_event)),
        }
    }
}
