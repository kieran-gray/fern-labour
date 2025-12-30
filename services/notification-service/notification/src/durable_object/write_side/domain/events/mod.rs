use fern_labour_event_sourcing_rs::{Event, StoredEvent};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::durable_object::write_side::domain::events::notification::{
    NotificationDelivered, NotificationDeliveryFailed, NotificationDispatched,
    NotificationRequested, RenderedContentStored,
};

pub mod notification;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(tag = "type", content = "data")]
pub enum NotificationEvent {
    NotificationRequested(NotificationRequested),
    RenderedContentStored(RenderedContentStored),
    NotificationDispatched(NotificationDispatched),
    NotificationDelivered(NotificationDelivered),
    NotificationDeliveryFailed(NotificationDeliveryFailed),
}

impl NotificationEvent {
    pub fn into_stored_event(self) -> StoredEvent {
        let event_str = serde_json::to_string(&self).unwrap();

        StoredEvent {
            aggregate_id: self.aggregate_id().to_string(),
            event_type: self.event_type().to_string(),
            event_data: event_str,
            event_version: self.event_version(),
        }
    }

    pub fn from_stored_event(event: StoredEvent) -> Self {
        serde_json::from_str(&event.event_data).unwrap()
    }
}

macro_rules! delegate_event_impl {
      ($($variant:ident),+ $(,)?) => {
          impl Event for NotificationEvent {
              fn event_type(&self) -> &str {
                  match self { $(NotificationEvent::$variant(e) => e.event_type(),)+ }
              }
              fn event_version(&self) -> i64 {
                  match self { $(NotificationEvent::$variant(e) => e.event_version(),)+ }
              }
              fn aggregate_id(&self) -> Uuid {
                  match self { $(NotificationEvent::$variant(e) => e.aggregate_id(),)+ }
              }
          }
      };
  }

delegate_event_impl!(
    NotificationRequested,
    RenderedContentStored,
    NotificationDispatched,
    NotificationDelivered,
    NotificationDeliveryFailed
);
