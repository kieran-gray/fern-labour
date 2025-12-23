use anyhow::{Result, anyhow};
use async_trait::async_trait;
use fern_labour_labour_shared::value_objects::LabourPhase;
use tracing::{info, warn};

use fern_labour_event_sourcing_rs::{AsyncProjector, AsyncRepositoryTrait, EventEnvelope};

use crate::durable_object::{
    read_side::read_models::labour_status::read_model::LabourStatusReadModel,
    write_side::domain::LabourEvent,
};

pub struct LabourStatusReadModelProjector {
    name: String,
    repository: Box<dyn AsyncRepositoryTrait<LabourStatusReadModel>>,
}

impl LabourStatusReadModelProjector {
    pub fn create(repository: Box<dyn AsyncRepositoryTrait<LabourStatusReadModel>>) -> Self {
        Self {
            name: "LabourStatusReadModelProjector".to_string(),
            repository,
        }
    }

    async fn project_event(
        &self,
        model: Option<LabourStatusReadModel>,
        envelope: &EventEnvelope<LabourEvent>,
    ) -> Option<LabourStatusReadModel> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            LabourEvent::LabourPlanned(e) if model.is_none() => Some(LabourStatusReadModel::new(
                e.labour_id,
                e.mother_id.clone(),
                e.mother_name.clone(),
                e.labour_name.clone(),
                timestamp,
            )),

            LabourEvent::LabourPlanUpdated(e) => {
                let mut labour = model?;
                labour.labour_name = e.labour_name.clone();
                labour.updated_at = timestamp;
                Some(labour)
            }

            LabourEvent::LabourBegun(_) => {
                let mut labour = model?;
                labour.current_phase = LabourPhase::EARLY;
                labour.updated_at = timestamp;
                Some(labour)
            }

            LabourEvent::LabourCompleted(_) => {
                let mut labour = model?;
                labour.current_phase = LabourPhase::COMPLETE;
                labour.updated_at = timestamp;
                Some(labour)
            }

            LabourEvent::LabourDeleted(e) => {
                if let Err(err) = self.repository.delete(e.labour_id).await {
                    warn!("Failed to delete LabourStatusReadModel: {err}")
                }
                None
            }
            _ => model,
        }
    }
}

#[async_trait(?Send)]
impl AsyncProjector<LabourEvent> for LabourStatusReadModelProjector {
    fn name(&self) -> &str {
        &self.name
    }

    async fn project_batch(&self, events: &[EventEnvelope<LabourEvent>]) -> Result<()> {
        if events.is_empty() {
            return Ok(());
        }

        let mut final_model = None;
        for envelope in events.iter() {
            final_model = self.project_event(final_model, envelope).await;
        }

        if let Some(model) = final_model {
            self.repository
                .overwrite(&model)
                .await
                .map_err(|err| anyhow!("Failed to persist LabourStatusReadModel: {err}"))?;

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
