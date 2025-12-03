use anyhow::{Result, anyhow};
use fern_labour_notifications_shared::value_objects::NotificationStatus;

use crate::application::webhook::ProviderStatusTranslator;

pub struct SendgridStatusTranslator;

impl ProviderStatusTranslator for SendgridStatusTranslator {
    fn provider_name(&self) -> &str {
        "sendgrid"
    }
    fn translate(&self, provider_event: &str) -> Result<NotificationStatus> {
        match provider_event {
            "deferred" | "processed" => Ok(NotificationStatus::SENT),
            "delivered" | "open" => Ok(NotificationStatus::DELIVERED),
            "bounce" | "dropped" => Ok(NotificationStatus::FAILED),
            _ => Err(anyhow!("Unknown sendgrid status: {}", provider_event)),
        }
    }
}
