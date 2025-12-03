use std::{collections::HashMap, rc::Rc};

use crate::{
    application::{dispatch::DispatchContext, dispatch::NotificationGatewayTrait},
    domain::{
        repository::TrackedNotificationRepositoryTrait, tracked_notification::TrackedNotification,
    },
};
use anyhow::{Context, Result, anyhow};
use chrono::Utc;
use fern_labour_notifications_shared::value_objects::NotificationChannel;
use tracing::error;

pub struct NotificationRouter {
    gateways: HashMap<NotificationChannel, Box<dyn NotificationGatewayTrait>>,
    repository: Rc<dyn TrackedNotificationRepositoryTrait>,
}

impl NotificationRouter {
    pub fn create(
        gateways: Vec<Box<dyn NotificationGatewayTrait>>,
        repository: Rc<dyn TrackedNotificationRepositoryTrait>,
    ) -> Self {
        let mut gateways_map = HashMap::new();

        for gateway in gateways {
            gateways_map.insert(gateway.channel(), gateway);
        }
        Self {
            gateways: gateways_map,
            repository,
        }
    }

    pub async fn dispatch(&self, context: DispatchContext) -> Result<Option<String>> {
        context.validate().context("Invalid dispatch context")?;
        let gateway = self.gateways.get(&context.channel()).ok_or_else(|| {
            anyhow!(
                "No gateway found for channel: {}. Available gateways: {:?}",
                context.channel(),
                self.gateways.keys().collect::<Vec<_>>()
            )
        })?;

        let external_id = gateway.dispatch(&context).await?;

        if let Some(ref id) = external_id {
            self.track_notification(&context, gateway.provider(), id)
                .await?;
        }

        Ok(external_id)
    }

    async fn track_notification(
        &self,
        context: &DispatchContext,
        provider: &str,
        external_id: &str,
    ) -> Result<()> {
        let tracked = TrackedNotification {
            notification_id: context.notification_id,
            external_id: external_id.to_string(),
            channel: context.channel(),
            provider: provider.to_string(),
            created_at: Utc::now(),
        };

        if let Err(err) = self.repository.put(&tracked).await {
            error!("Failed to store tracked notification in DB: {err}")
        };

        Ok(())
    }
}
