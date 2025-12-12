use anyhow::Result;
use async_trait::async_trait;
use fern_labour_labour_shared::value_objects::contraction::duration::Duration;

use fern_labour_event_sourcing_rs::{EventEnvelope, SyncProjector, SyncRepositoryTrait};

use crate::durable_object::{
    read_side::read_models::contractions::ContractionReadModel, write_side::domain::LabourEvent,
};

pub struct ContractionReadModelProjector {
    name: String,
    repository: Box<dyn SyncRepositoryTrait<ContractionReadModel>>,
}

impl ContractionReadModelProjector {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<ContractionReadModel>>) -> Self {
        Self {
            name: "ContractionReadModelProjector".to_string(),
            repository,
        }
    }

    fn project_event(&self, envelope: &EventEnvelope<LabourEvent>) -> Result<()> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            LabourEvent::ContractionStarted {
                labour_id,
                contraction_id,
                start_time,
            } => {
                let contraction = ContractionReadModel::new(
                    *labour_id,
                    *contraction_id,
                    Duration::create(*start_time, *start_time)?,
                    None,
                    timestamp,
                );
                self.repository.overwrite(&contraction)
            }
            LabourEvent::ContractionEnded {
                contraction_id,
                end_time,
                intensity,
                ..
            } => {
                let mut contraction = self
                    .repository
                    .get_by_id(*contraction_id)
                    .unwrap_or_else(|_| panic!("No contraction found with id: {contraction_id}"));
                contraction.duration =
                    Duration::create(*contraction.duration.start_time(), *end_time)
                        .expect("Failed to create duration");
                contraction.intensity = Some(*intensity);
                contraction.updated_at = timestamp;
                self.repository.upsert(&contraction)
            }
            LabourEvent::ContractionDeleted { contraction_id, .. } => {
                self.repository.delete(*contraction_id)
            }
            _ => Ok(()),
        }
    }
}

#[async_trait(?Send)]
impl SyncProjector<LabourEvent> for ContractionReadModelProjector {
    fn name(&self) -> &str {
        &self.name
    }

    fn project_batch(&self, events: &[EventEnvelope<LabourEvent>]) -> Result<()> {
        if events.is_empty() {
            return Ok(());
        }

        events
            .iter()
            .try_for_each(|envelope| self.project_event(envelope))
    }
}
