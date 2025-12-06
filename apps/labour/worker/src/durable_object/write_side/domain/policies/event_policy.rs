use fern_labour_notifications_shared::ServiceCommand;

use crate::durable_object::write_side::domain::{Labour, NotificationEvent};

pub trait EventPolicy {
    fn handle(&self, event: &NotificationEvent, aggregate: Option<&Labour>) -> Vec<ServiceCommand>;
}
