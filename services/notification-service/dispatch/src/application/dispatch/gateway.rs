use anyhow::Result;
use async_trait::async_trait;
use fern_labour_notifications_shared::value_objects::NotificationChannel;

use super::context::DispatchContext;

#[async_trait(?Send)]
pub trait NotificationGatewayTrait: Send + Sync {
    fn channel(&self) -> NotificationChannel;

    fn provider(&self) -> &str;

    async fn dispatch(&self, context: &DispatchContext) -> Result<Option<String>>;
}
