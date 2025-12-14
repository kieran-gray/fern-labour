use std::rc::Rc;

use anyhow::{Context, Result};
use chrono::NaiveDateTime;
use fern_labour_event_sourcing_rs::{Event, EventEnvelope, EventMetadata, EventStoreTrait};

use crate::durable_object::write_side::domain::LabourEvent;

pub struct EventQuery {
    event_store: Rc<dyn EventStoreTrait>,
}

impl EventQuery {
    pub fn new(event_store: Rc<dyn EventStoreTrait>) -> Self {
        Self { event_store }
    }

    pub fn get_event_stream(&self) -> Result<Vec<EventEnvelope<LabourEvent>>> {
        let stored_events = self
            .event_store
            .load()
            .context("Failed to load events from store")?;

        if stored_events.is_empty() {
            return Ok(vec![]);
        }

        let envelopes: Vec<EventEnvelope<LabourEvent>> = stored_events
            .into_iter()
            .map(|stored| {
                let event: LabourEvent = serde_json::from_str(&stored.event_data)
                    .context("Failed to deserialize notification event")?;

                let timestamp =
                    NaiveDateTime::parse_from_str(&stored.created_at, "%Y-%m-%d %H:%M:%S")
                        .context("Failed to parse created_at timestamp")?
                        .and_utc();

                let metadata = EventMetadata {
                    aggregate_id: event.aggregate_id(),
                    sequence: stored.sequence,
                    event_version: stored.event_version,
                    timestamp,
                    user_id: stored.user_id,
                };

                Ok(EventEnvelope { metadata, event })
            })
            .collect::<Result<Vec<_>>>()?;

        Ok(envelopes)
    }
}
