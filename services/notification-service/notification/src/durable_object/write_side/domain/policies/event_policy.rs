use fern_labour_notifications_shared::ServiceCommand;

use crate::durable_object::write_side::domain::{Notification, NotificationEvent};

pub trait EventPolicy {
    fn handle(
        &self,
        event: &NotificationEvent,
        aggregate: Option<&Notification>,
    ) -> Vec<ServiceCommand>;
}
