use std::rc::Rc;

use anyhow::{Context, Result};
use fern_labour_event_sourcing_rs::{AggregateRepositoryTrait, EventEnvelope};

use crate::durable_object::write_side::domain::{Labour, LabourEvent};

pub struct EventQuery {
    aggregate_repository: Rc<dyn AggregateRepositoryTrait<Labour>>,
}

impl EventQuery {
    pub fn new(aggregate_repository: Rc<dyn AggregateRepositoryTrait<Labour>>) -> Self {
        Self {
            aggregate_repository,
        }
    }

    pub fn get_event_stream(&self) -> Result<Vec<EventEnvelope<LabourEvent>>> {
        let events = self
            .aggregate_repository
            .load_events()
            .context("Failed to load events from repo")?;

        Ok(events)
    }
}
