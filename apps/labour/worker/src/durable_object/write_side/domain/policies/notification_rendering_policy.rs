use fern_labour_notifications_shared::ServiceCommand;
use tracing::debug;

use crate::durable_object::write_side::domain::{
    Labour, NotificationEvent, policies::EventPolicy,
};

pub struct NotificationRenderingPolicy;

impl EventPolicy for NotificationRenderingPolicy {
    fn handle(
        &self,
        event: &NotificationEvent,
        _aggregate: Option<&Labour>,
    ) -> Vec<ServiceCommand> {
        match event {
            NotificationEvent::NotificationRequested {
                notification_id,
                channel,
                template_data,
                ..
            } => {
                debug!(
                    notification_id = %notification_id,
                    channel = %channel,
                    "NotificationRenderingPolicy triggered - generating RenderNotification service command"
                );
                vec![ServiceCommand::RenderNotification {
                    notification_id: *notification_id,
                    channel: channel.clone(),
                    template_data: template_data.clone(),
                }]
            }
            _ => vec![],
        }
    }
}
