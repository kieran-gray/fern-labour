use anyhow::{Result, anyhow};
use fern_labour_labour_shared::value_objects::LabourPhase;
use tracing::info;

use fern_labour_event_sourcing_rs::{EventEnvelope, SyncProjector, SyncRepositoryTrait};
use uuid::Uuid;

use crate::durable_object::{
    read_side::read_models::labour::read_model::LabourReadModel, write_side::domain::LabourEvent,
};

pub struct LabourReadModelProjector {
    name: String,
    repository: Box<dyn SyncRepositoryTrait<LabourReadModel>>,
}

impl LabourReadModelProjector {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<LabourReadModel>>) -> Self {
        Self {
            name: "LabourReadModelProjector".to_string(),
            repository,
        }
    }

    fn fetch_labour(&self, labour_id: Uuid) -> LabourReadModel {
        self.repository
            .get_by_id(labour_id)
            .expect("Labour must exist here")
    }

    fn project_event(
        &self,
        model: Option<LabourReadModel>,
        envelope: &EventEnvelope<LabourEvent>,
    ) -> Option<LabourReadModel> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            LabourEvent::LabourPlanned(e) if model.is_none() => Some(LabourReadModel::new(
                e.labour_id,
                e.mother_id.clone(),
                e.mother_name.clone(),
                e.first_labour,
                e.due_date,
                e.labour_name.clone(),
                timestamp,
            )),

            LabourEvent::LabourPlanUpdated(e) => {
                let mut labour = match model {
                    Some(model) => model,
                    None => self.fetch_labour(e.labour_id),
                };

                labour.first_labour = e.first_labour;
                labour.due_date = e.due_date;
                labour.labour_name = e.labour_name.clone();
                Some(labour)
            }

            LabourEvent::LabourBegun(e) => {
                let mut labour = match model {
                    Some(model) => model,
                    None => self.fetch_labour(e.labour_id),
                };

                labour.start_time = Some(e.start_time);
                labour.current_phase = LabourPhase::EARLY;
                Some(labour)
            }

            LabourEvent::LabourCompleted(e) => {
                let mut labour = match model {
                    Some(model) => model,
                    None => self.fetch_labour(e.labour_id),
                };

                labour.end_time = Some(e.end_time);
                labour.notes = e.notes.clone();
                labour.current_phase = LabourPhase::COMPLETE;
                Some(labour)
            }

            _ => model,
        }
    }
}

impl SyncProjector<LabourEvent> for LabourReadModelProjector {
    fn name(&self) -> &str {
        &self.name
    }

    fn project_batch(&self, events: &[EventEnvelope<LabourEvent>]) -> Result<()> {
        if events.is_empty() {
            return Ok(());
        }

        let final_model = events
            .iter()
            .fold(None, |model, envelope| self.project_event(model, envelope));

        if let Some(model) = final_model {
            self.repository
                .overwrite(&model)
                .map_err(|err| anyhow!("Failed to persist LabourReadModel: {err}"))?;

            info!(
                projector = %self.name,
                labour_id = %model.labour_id,
                events_processed = events.len(),
                "Persisted read model after batch processing"
            );
        }

        Ok(())
    }
}
