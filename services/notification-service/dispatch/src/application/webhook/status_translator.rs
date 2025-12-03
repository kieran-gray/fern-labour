use anyhow::Result;
use fern_labour_notifications_shared::value_objects::NotificationStatus;

pub trait ProviderStatusTranslator {
    fn provider_name(&self) -> &str;
    fn translate(&self, provider_event: &str) -> Result<NotificationStatus>;
}
