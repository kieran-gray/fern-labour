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
            LabourEvent::LabourPlanned {
                labour_id,
                birthing_person_id,
                first_labour,
                due_date,
                labour_name,
            } if model.is_none() => Some(LabourReadModel::new(
                *labour_id,
                birthing_person_id.clone(),
                *first_labour,
                *due_date,
                labour_name.clone(),
                timestamp,
            )),

            LabourEvent::LabourPlanUpdated {
                labour_id,
                first_labour,
                due_date,
                labour_name,
            } => {
                let mut labour = match model {
                    Some(model) => model,
                    None => self.fetch_labour(*labour_id),
                };

                labour.first_labour = *first_labour;
                labour.due_date = *due_date;
                labour.labour_name = labour_name.clone();
                Some(labour)
            }

            LabourEvent::LabourBegun {
                labour_id,
                start_time,
            } => {
                let mut labour = match model {
                    Some(model) => model,
                    None => self.fetch_labour(*labour_id),
                };

                labour.start_time = Some(*start_time);
                labour.current_phase = LabourPhase::EARLY;
                Some(labour)
            }

            LabourEvent::LabourCompleted {
                labour_id,
                end_time,
            } => {
                let mut labour = match model {
                    Some(model) => model,
                    None => self.fetch_labour(*labour_id),
                };

                labour.end_time = Some(*end_time);
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
