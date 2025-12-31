use std::{marker::PhantomData, rc::Rc};

use anyhow::{Context, Result};
use serde::{Serialize, de::DeserializeOwned};
use tracing::debug;

use crate::{
    Aggregate, AppendResult, CacheExt, CacheTrait, Event, EventEnvelope, EventEnvelopeAdapter,
    EventStoreTrait, StoredEvent,
};

pub trait AggregateRepositoryTrait<A: Aggregate> {
    fn load(&self) -> Result<Option<A>>;
    fn load_events(&self) -> Result<Vec<EventEnvelope<A::Event>>>;
    fn save(
        &self,
        aggregate: Option<&A>,
        events: &[A::Event],
        user_id: String,
    ) -> Result<Vec<AppendResult>>;
    fn save_with_envelopes(
        &self,
        aggregate: Option<&A>,
        events: &[A::Event],
        user_id: String,
    ) -> Result<Vec<EventEnvelope<A::Event>>>;
}

#[derive(Clone)]
pub struct AggregateRepository<A: Aggregate> {
    event_store: Rc<dyn EventStoreTrait>,
    _phantom: PhantomData<A>,
}

impl<A: Aggregate> AggregateRepository<A> {
    pub fn new(event_store: Rc<dyn EventStoreTrait>) -> Self {
        Self {
            event_store,
            _phantom: PhantomData,
        }
    }
}

impl<A: Aggregate> AggregateRepositoryTrait<A> for AggregateRepository<A>
where
    A::Event: DeserializeOwned + Serialize + Event,
{
    fn load(&self) -> Result<Option<A>> {
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

    fn load_events(&self) -> Result<Vec<EventEnvelope<A::Event>>> {
        let stored_events = self
            .event_store
            .load()
            .context("Failed to load events from store")?;

        stored_events
            .into_iter()
            .map(|stored| stored.to_envelope())
            .collect()
    }

    fn save(
        &self,
        _aggregate: Option<&A>,
        events: &[A::Event],
        user_id: String,
    ) -> Result<Vec<AppendResult>> {
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

    fn save_with_envelopes(
        &self,
        _aggregate: Option<&A>,
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

#[derive(Clone)]
pub struct CachedAggregateRepository<A: Aggregate> {
    event_store: Rc<dyn EventStoreTrait>,
    cache: Rc<dyn CacheTrait>,
    cache_key: String,
    _phantom: PhantomData<A>,
}

impl<A: Aggregate> CachedAggregateRepository<A>
where
    A::Event: DeserializeOwned + Serialize + Event,
{
    pub fn new(
        event_store: Rc<dyn EventStoreTrait>,
        cache: Rc<dyn CacheTrait>,
        cache_key: String,
    ) -> Self {
        Self {
            event_store,
            cache,
            cache_key,
            _phantom: PhantomData,
        }
    }

    fn load_from_event_store(&self) -> Result<Option<A>> {
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
}

impl<A: Aggregate> AggregateRepositoryTrait<A> for CachedAggregateRepository<A>
where
    A::Event: DeserializeOwned + Serialize + Event,
{
    fn load(&self) -> Result<Option<A>> {
        if let Ok(Some(aggregate)) = self.cache.get::<A>(self.cache_key.clone()) {
            debug!(cache_key = %self.cache_key, "Aggregate cache HIT");
            return Ok(Some(aggregate));
        };

        debug!(cache_key = %self.cache_key, "Aggregate cache MISS - loading from event store");
        self.load_from_event_store()
    }

    fn load_events(&self) -> Result<Vec<EventEnvelope<A::Event>>> {
        let stored_events = self
            .event_store
            .load()
            .context("Failed to load events from store")?;

        stored_events
            .into_iter()
            .map(|stored| stored.to_envelope())
            .collect()
    }

    fn save(
        &self,
        aggregate: Option<&A>,
        events: &[A::Event],
        user_id: String,
    ) -> Result<Vec<AppendResult>> {
        debug!(cache_key = %self.cache_key, "Clearing aggregate cache before save");
        let _ = self.cache.clear(self.cache_key.clone());

        let mut results = Vec::new();
        for event in events {
            let stored: StoredEvent = event.clone().into_stored_event();
            let result =
                self.event_store
                    .append(stored.aggregate_id.clone(), stored, user_id.clone())?;
            results.push(result);
        }

        if let Some(agg) = aggregate {
            debug!(cache_key = %self.cache_key, "Caching updated aggregate after save");
            if let Err(e) = self.cache.set(self.cache_key.clone(), agg) {
                debug!(cache_key = %self.cache_key, error = %e, "Failed to cache aggregate - will rebuild from events on next load");
            }
        }

        Ok(results)
    }

    fn save_with_envelopes(
        &self,
        aggregate: Option<&A>,
        events: &[A::Event],
        user_id: String,
    ) -> Result<Vec<EventEnvelope<A::Event>>> {
        debug!(cache_key = %self.cache_key, "Clearing aggregate cache before save");
        let _ = self.cache.clear(self.cache_key.clone());

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

        if let Some(agg) = aggregate {
            debug!(cache_key = %self.cache_key, "Caching updated aggregate after save");
            if let Err(e) = self.cache.set(self.cache_key.clone(), agg) {
                debug!(cache_key = %self.cache_key, error = %e, "Failed to cache aggregate - will rebuild from events on next load");
            }
        }

        Ok(envelopes)
    }
}
