use std::rc::Rc;

use anyhow::{Context, Result, anyhow};
use tracing::{debug, info, warn};

use fern_labour_event_sourcing_rs::{
    CacheTrait, EventEnvelope, EventEnvelopeAdapter, EventStoreTrait, IncrementalAsyncProjector,
};

use crate::durable_object::write_side::domain::LabourEvent;

pub struct AsyncProjectionProcessor {
    event_store: Rc<dyn EventStoreTrait>,
    cache: Rc<dyn CacheTrait>,
    projectors: Vec<Box<dyn IncrementalAsyncProjector<LabourEvent>>>,
    default_batch_size: i64,
}

impl AsyncProjectionProcessor {
    pub fn create(
        event_store: Rc<dyn EventStoreTrait>,
        cache: Rc<dyn CacheTrait>,
        projectors: Vec<Box<dyn IncrementalAsyncProjector<LabourEvent>>>,
        default_batch_size: i64,
    ) -> Self {
        Self {
            event_store,
            cache,
            projectors,
            default_batch_size,
        }
    }

    fn get_min_cached_sequence(&self) -> i64 {
        self.projectors
            .iter()
            .map(|p| p.get_cached_sequence(&self.cache))
            .min()
            .unwrap_or(0)
    }

    pub async fn process_projections(&self) -> Result<()> {
        debug!("Starting async projection processing");

        let Some(max_sequence) = self.event_store.max_sequence()? else {
            debug!("No events in store");
            return Ok(());
        };

        let min_cached_sequence = self.get_min_cached_sequence();

        if min_cached_sequence >= max_sequence {
            debug!(
                min_cached_sequence = min_cached_sequence,
                max_sequence = max_sequence,
                "All projectors are up to date, skipping"
            );
            return Ok(());
        }

        let stored_events = self
            .event_store
            .events_since(min_cached_sequence, self.default_batch_size)
            .context("Failed to fetch events since checkpoint")?;

        if stored_events.is_empty() {
            debug!("No new events to process");
            return Ok(());
        }

        let envelopes: Vec<EventEnvelope<LabourEvent>> = stored_events
            .into_iter()
            .map(|stored| stored.to_envelope())
            .collect::<Result<Vec<_>>>()?;

        debug!(
            event_count = envelopes.len(),
            min_cached_sequence = min_cached_sequence,
            max_sequence = max_sequence,
            "Processing events through incremental projectors"
        );

        for projector in &self.projectors {
            if let Err(e) = projector
                .process(&self.cache, &envelopes, max_sequence)
                .await
            {
                warn!(
                    projector = %projector.name(),
                    error = %e,
                    "Failed to process projector"
                );
                return Err(anyhow!(
                    "Failed to process projector {}: {}",
                    projector.name(),
                    e
                ));
            }
        }

        info!(
            projector_count = self.projectors.len(),
            events_loaded = envelopes.len(),
            max_sequence = max_sequence,
            "Async projection processing completed"
        );

        Ok(())
    }
}
