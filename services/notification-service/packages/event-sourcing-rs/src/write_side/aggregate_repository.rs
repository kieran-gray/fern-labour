use std::{marker::PhantomData, rc::Rc};

use anyhow::{Context, Result};
use serde::{Serialize, de::DeserializeOwned};

use crate::{Aggregate, AppendResult, Event, EventEnvelope, EventStoreTrait, StoredEvent};

#[derive(Clone)]
pub struct AggregateRepository<A: Aggregate> {
    event_store: Rc<dyn EventStoreTrait>,
    _phantom: PhantomData<A>,
}

impl<A: Aggregate> AggregateRepository<A>
where
    A::Event: DeserializeOwned + Serialize + Event,
{
    pub fn new(event_store: Rc<dyn EventStoreTrait>) -> Self {
        Self {
            event_store,
            _phantom: PhantomData,
        }
    }

    pub fn load(&self) -> Result<Option<A>> {
        let stored_events = self
            .event_store
            .load()
            .context("Failed to load events from store")?;

        if stored_events.is_empty() {
            return Ok(None);
        }

        let events: Vec<A::Event> = stored_events
            .into_iter()
            .map(|stored| {
                serde_json::from_str(&stored.event_data).context("Failed to deserialize event")
            })
            .collect::<Result<Vec<_>>>()?;

        Ok(A::from_events(&events))
    }

    pub fn save(&self, events: &[A::Event], user_id: String) -> Result<Vec<AppendResult>> {
        let mut results = Vec::new();
        for event in events {
            let stored: StoredEvent = event.clone().into_stored_event();
            let result =
                self.event_store
                    .append(stored.aggregate_id.clone(), stored, user_id.clone())?;
            results.push(result);
        }
        Ok(results)
    }

    pub fn save_with_envelopes(
        &self,
        events: &[A::Event],
        user_id: String,
    ) -> Result<Vec<EventEnvelope<A::Event>>> {
        let mut envelopes = Vec::new();
        for event in events {
            let stored: StoredEvent = event.clone().into_stored_event();
            let result =
                self.event_store
                    .append(stored.aggregate_id.clone(), stored, user_id.clone())?;
            envelopes.push(EventEnvelope::enrich(
                event.clone(),
                &result,
                user_id.clone(),
            ));
        }
        Ok(envelopes)
    }
}
