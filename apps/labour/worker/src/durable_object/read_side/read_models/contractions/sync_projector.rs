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
            LabourEvent::ContractionStarted(e) => {
                let contraction = ContractionReadModel::new(
                    e.labour_id,
                    e.contraction_id,
                    Duration::create(e.start_time, e.start_time)?,
                    None,
                    timestamp,
                );
                self.repository.overwrite(&contraction)
            }
            LabourEvent::ContractionEnded(e) => {
                let mut contraction =
                    self.repository
                        .get_by_id(e.contraction_id)
                        .unwrap_or_else(|_| {
                            panic!("No contraction found with id: {}", e.contraction_id)
                        });
                let duration = Duration::create(*contraction.duration.start_time(), e.end_time)?;
                contraction.duration_seconds = duration.duration_seconds();
                contraction.duration = duration;
                contraction.intensity = Some(e.intensity);
                contraction.updated_at = timestamp;
                self.repository.upsert(&contraction)
            }
            LabourEvent::ContractionDeleted(e) => self.repository.delete(e.contraction_id),
            LabourEvent::ContractionUpdated(e) => {
                let mut contraction =
                    self.repository
                        .get_by_id(e.contraction_id)
                        .unwrap_or_else(|_| {
                            panic!("No contraction found with id: {}", e.contraction_id)
                        });
                let new_start_time = match &e.start_time {
                    Some(start_time) => *start_time,
                    None => *contraction.duration.start_time(),
                };
                let new_end_time = match &e.end_time {
                    Some(end_time) => *end_time,
                    None => *contraction.duration.end_time(),
                };
                let duration = Duration::create(new_start_time, new_end_time)?;
                contraction.duration_seconds = duration.duration_seconds();
                contraction.duration = duration;
                contraction.intensity = e.intensity;
                self.repository.upsert(&contraction)
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
