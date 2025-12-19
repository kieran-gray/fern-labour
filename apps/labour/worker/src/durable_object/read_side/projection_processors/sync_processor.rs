use std::collections::HashMap;
use std::rc::Rc;

use anyhow::{Context, Result, anyhow};
use tracing::{error, info};

use fern_labour_event_sourcing_rs::{
    CheckpointRepository, CheckpointStatus, EventEnvelopeAdapter, EventStoreTrait,
    ProjectionCheckpoint, SyncProjector,
};

use crate::durable_object::write_side::domain::LabourEvent;

const DEFAULT_BATCH_SIZE: i64 = 100;

pub struct SyncProjectionProcessor {
    event_store: Rc<dyn EventStoreTrait>,
    checkpoint_repository: Box<dyn CheckpointRepository>,
    projectors: HashMap<String, Box<dyn SyncProjector<LabourEvent>>>,
    batch_size: i64,
}

impl SyncProjectionProcessor {
    pub fn create(
        event_store: Rc<dyn EventStoreTrait>,
        checkpoint_repository: Box<dyn CheckpointRepository>,
        projectors: Vec<Box<dyn SyncProjector<LabourEvent>>>,
    ) -> Self {
        let projector_map: HashMap<String, Box<dyn SyncProjector<LabourEvent>>> = projectors
            .into_iter()
            .map(|proj| (proj.name().to_string(), proj))
            .collect();

        Self {
            event_store,
            checkpoint_repository,
            projectors: projector_map,
            batch_size: DEFAULT_BATCH_SIZE,
        }
    }

    pub fn process_projections(&self) -> Result<()> {
        info!("Starting checkpoint-based projection processing");

        for (projector_name, projector) in &self.projectors {
            if let Err(e) = self.process_single_projector(projector_name, projector.as_ref()) {
                error!(
                    projector = %projector_name,
                    error = %e,
                    "Failed to process projector"
                );
            }
        }

        Ok(())
    }

    fn process_single_projector(
        &self,
        projector_name: &str,
        projector: &dyn SyncProjector<LabourEvent>,
    ) -> Result<()> {
        let checkpoint = self
            .checkpoint_repository
            .get_checkpoint(projector_name)?
            .unwrap_or_else(|| self.create_initial_checkpoint(projector_name));

        let last_sequence = checkpoint.last_processed_sequence;

        info!(
            projector = %projector_name,
            last_sequence = last_sequence,
            "Processing projector from checkpoint"
        );

        let stored_events = self
            .event_store
            .events_since(last_sequence, self.batch_size)
            .context("Failed to fetch events since checkpoint")?;

        if stored_events.is_empty() {
            info!(
                projector = %projector_name,
                "No new events to process"
            );
            return Ok(());
        }

        let envelopes = stored_events
            .iter()
            .map(|stored| stored.to_envelope())
            .collect::<Result<Vec<_>>>()?;

        let event_count = envelopes.len();
        info!(
            projector = %projector_name,
            event_count = event_count,
            "Processing events"
        );

        projector
            .project_batch(&envelopes)
            .map_err(|err| anyhow!("Projector {projector_name} failed to process batch: {err}",))?;

        let last_envelope = envelopes.last().unwrap();
        let new_checkpoint = ProjectionCheckpoint {
            projector_name: projector_name.to_string(),
            last_processed_sequence: last_envelope.metadata.sequence,
            last_processed_at: last_envelope.metadata.timestamp,
            updated_at: chrono::Utc::now(),
            status: CheckpointStatus::Healthy,
            error_message: None,
            error_count: 0,
        };

        self.checkpoint_repository
            .update_checkpoint(&new_checkpoint)
            .context("Failed to update checkpoint")?;

        info!(
            projector = %projector_name,
            events_processed = event_count,
            new_sequence = new_checkpoint.last_processed_sequence,
            "Successfully processed and checkpointed events"
        );

        Ok(())
    }

    fn create_initial_checkpoint(&self, projector_name: &str) -> ProjectionCheckpoint {
        ProjectionCheckpoint {
            projector_name: projector_name.to_string(),
            last_processed_sequence: 0,
            last_processed_at: chrono::Utc::now(),
            updated_at: chrono::Utc::now(),
            status: CheckpointStatus::Healthy,
            error_message: None,
            error_count: 0,
        }
    }

    pub fn get_last_processed_sequence(&self) -> i64 {
        self.projectors
            .keys()
            .filter_map(|projector_name| {
                self.checkpoint_repository
                    .get_checkpoint(projector_name)
                    .ok()
                    .flatten()
                    .map(|cp| cp.last_processed_sequence)
            })
            .min()
            .unwrap_or(0)
    }
}
