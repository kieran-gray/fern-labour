use anyhow::Result;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::fmt::Debug;
use uuid::Uuid;

use crate::event_store::{AppendResult, StoredEvent};

pub trait Event: Debug + Clone + Serialize + for<'de> Deserialize<'de> + Send + Sync {
    fn event_type(&self) -> &str;
    fn event_version(&self) -> i64;
    fn aggregate_id(&self) -> Uuid;

    fn into_stored_event(self) -> StoredEvent
    where
        Self: Sized,
    {
        let event_str = serde_json::to_string(&self).unwrap();

        StoredEvent {
            aggregate_id: self.aggregate_id().to_string(),
            event_type: self.event_type().to_string(),
            event_data: event_str,
            event_version: self.event_version(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EventMetadata {
    pub aggregate_id: Uuid,
    pub sequence: i64,
    pub event_version: i64,
    pub timestamp: DateTime<Utc>,
    pub user_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EventEnvelope<E> {
    pub metadata: EventMetadata,
    pub event: E,
}

impl<E: Event> EventEnvelope<E> {
    pub fn enrich(event: E, append_result: &AppendResult, user_id: String) -> Self {
        let event_metadata = EventMetadata {
            aggregate_id: event.aggregate_id(),
            sequence: append_result.sequence,
            event_version: event.event_version(),
            timestamp: append_result.timestamp,
            user_id,
        };

        EventEnvelope {
            metadata: event_metadata,
            event,
        }
    }
}

pub trait EventEnvelopeAdapter<E: Event> {
    fn to_envelope(&self) -> Result<EventEnvelope<E>>;
}

#[macro_export]
macro_rules! impl_event {
    ($name:ident, $id_field:ident) => {
        impl Event for $name {
            fn aggregate_id(&self) -> Uuid {
                self.$id_field
            }
            fn event_type(&self) -> &str {
                stringify!($name)
            }
            fn event_version(&self) -> i64 {
                1
            }
        }
    };

    ($name:ident, $id_field:ident, $version:expr) => {
        impl Event for $name {
            fn aggregate_id(&self) -> Uuid {
                self.$id_field
            }
            fn event_type(&self) -> &str {
                stringify!($name)
            }
            fn event_version(&self) -> i64 {
                $version
            }
        }
    };
}
