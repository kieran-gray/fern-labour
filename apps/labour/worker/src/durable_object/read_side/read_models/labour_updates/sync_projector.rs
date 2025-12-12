use anyhow::Result;
use async_trait::async_trait;

use fern_labour_event_sourcing_rs::{EventEnvelope, SyncProjector, SyncRepositoryTrait};

use crate::durable_object::{
    read_side::read_models::labour_updates::LabourUpdateReadModel, write_side::domain::LabourEvent,
};

pub struct LabourUpdateReadModelProjector {
    name: String,
    repository: Box<dyn SyncRepositoryTrait<LabourUpdateReadModel>>,
}

impl LabourUpdateReadModelProjector {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<LabourUpdateReadModel>>) -> Self {
        Self {
            name: "LabourUpdateReadModelProjector".to_string(),
            repository,
        }
    }

    fn project_event(&self, envelope: &EventEnvelope<LabourEvent>) -> Result<()> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            LabourEvent::LabourUpdatePosted {
                labour_id,
                labour_update_id,
                labour_update_type,
                message,
                application_generated,
                sent_time,
            } => {
                let labour_update = LabourUpdateReadModel::new(
                    *labour_id,
                    *labour_update_id,
                    labour_update_type.clone(),
                    message.clone(),
                    *application_generated,
                    *sent_time,
                );
                self.repository.overwrite(&labour_update)
            }
            LabourEvent::LabourUpdateMessageUpdated {
                labour_update_id,
                message,
                ..
            } => {
                let mut labour_update = self
                    .repository
                    .get_by_id(*labour_update_id)
                    .unwrap_or_else(|_| {
                        panic!("No labour_update found with id: {labour_update_id}")
                    });
                labour_update.message = message.clone();
                labour_update.edited = true;
                labour_update.updated_at = timestamp;
                self.repository.upsert(&labour_update)
            }
            LabourEvent::LabourUpdateTypeUpdated {
                labour_update_id,
                labour_update_type,
                ..
            } => {
                let mut labour_update = self
                    .repository
                    .get_by_id(*labour_update_id)
                    .unwrap_or_else(|_| {
                        panic!("No labour_update found with id: {labour_update_id}")
                    });
                labour_update.labour_update_type = labour_update_type.clone();
                labour_update.updated_at = timestamp;
                self.repository.upsert(&labour_update)
            }
            LabourEvent::LabourUpdateDeleted {
                labour_update_id, ..
            } => self.repository.delete(*labour_update_id),
            _ => Ok(()),
        }
    }
}

#[async_trait(?Send)]
impl SyncProjector<LabourEvent> for LabourUpdateReadModelProjector {
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
