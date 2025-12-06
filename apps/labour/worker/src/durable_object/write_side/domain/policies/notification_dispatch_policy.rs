use fern_labour_notifications_shared::ServiceCommand;
use tracing::{debug, warn};

use crate::durable_object::write_side::domain::{
    Labour, NotificationEvent, policies::EventPolicy,
};

pub struct NotificationDispatchPolicy;

impl EventPolicy for NotificationDispatchPolicy {
    fn handle(
        &self,
        event: &NotificationEvent,
        aggregate: Option<&Labour>,
    ) -> Vec<ServiceCommand> {
        match event {
            NotificationEvent::RenderedContentStored {
                notification_id,
                rendered_content: rendered_template,
            } => {
                if let Some(notif) = aggregate {
                    debug!(
                        notification_id = %notification_id,
                        channel = %notif.channel(),
                        destination = %notif.destination(),
                        "NotificationDispatchPolicy triggered - generating DispatchNotification service command"
                    );
                    vec![ServiceCommand::DispatchNotification {
                        notification_id: *notification_id,
                        channel: notif.channel().clone(),
                        destination: notif.destination().clone(),
                        rendered_content: rendered_template.clone(),
                    }]
                } else {
                    warn!(
                        notification_id = %notification_id,
                        "NotificationDispatchPolicy: aggregate is None, cannot dispatch - no commands generated"
                    );
                    vec![]
                }
            }
            _ => vec![],
        }
    }
}
