use anyhow::{Result, anyhow};
use fern_labour_notifications_shared::value_objects::NotificationStatus;

use crate::application::webhook::ProviderStatusTranslator;

pub struct TwilioStatusTranslator;

impl ProviderStatusTranslator for TwilioStatusTranslator {
    fn provider_name(&self) -> &str {
        "twilio"
    }
    fn translate(&self, provider_event: &str) -> Result<NotificationStatus> {
        match provider_event {
            "queued" | "sent" => Ok(NotificationStatus::SENT),
            "delivered" | "read" => Ok(NotificationStatus::DELIVERED),
            "cancelled" | "failed" | "undelivered" => Ok(NotificationStatus::FAILED),
            _ => Err(anyhow!("Unknown twilio status: {}", provider_event)),
        }
    }
}
