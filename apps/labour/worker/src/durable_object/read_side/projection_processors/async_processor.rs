use std::{collections::HashMap, rc::Rc};

use anyhow::{Context, Result, anyhow};
use futures::future::try_join_all;
use tracing::info;

use fern_labour_event_sourcing_rs::{
    AsyncProjector, EventEnvelope, EventEnvelopeAdapter, EventStoreTrait,
};

use crate::durable_object::write_side::domain::LabourEvent;

pub struct AsyncProjectionProcessor {
    event_store: Rc<dyn EventStoreTrait>,
    projectors: HashMap<String, Box<dyn AsyncProjector<LabourEvent>>>,
}

impl AsyncProjectionProcessor {
    pub fn create(
        event_store: Rc<dyn EventStoreTrait>,
        projectors: Vec<Box<dyn AsyncProjector<LabourEvent>>>,
    ) -> Self {
        let projector_map: HashMap<String, Box<dyn AsyncProjector<LabourEvent>>> = projectors
            .into_iter()
            .map(|proj| (proj.name().to_string(), proj))
            .collect();
        Self {
            event_store,
            projectors: projector_map,
        }
    }

    pub async fn process_projections(&self) -> Result<()> {
        info!("Starting projection processing");

        let stored_events = self
            .event_store
            .load()
            .context("Failed to load events from store")?;

        if stored_events.is_empty() {
            info!("No events to project");
            return Ok(());
        }

        let envelopes: Vec<EventEnvelope<LabourEvent>> = stored_events
            .into_iter()
            .map(|stored| stored.to_envelope())
            .collect::<Result<Vec<_>>>()?;

        let event_count = envelopes.len();
        info!(
            event_count = event_count,
            "Processing events through projectors"
        );

        let futures: Vec<_> = self
            .projectors
            .values()
            .map(|projector| projector.project_batch(&envelopes))
            .collect();

        try_join_all(futures)
            .await
            .map_err(|err| anyhow!("Failed to project events: {err}"))?;

        info!(
            events_processed = event_count,
            "Projection processing completed"
        );

        Ok(())
    }
}
