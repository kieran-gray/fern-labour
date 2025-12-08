use anyhow::{Result, anyhow};
use async_trait::async_trait;
use fern_labour_labour_shared::value_objects::LabourPhase;
use tracing::info;

use fern_labour_event_sourcing_rs::{EventEnvelope, Projector, RepositoryTrait};

use crate::durable_object::{
    read_side::read_models::contractions::ContractionReadModel, write_side::domain::LabourEvent,
};

pub struct ContractionReadModelProjector {
    name: String,
    repository: Box<dyn RepositoryTrait<ContractionReadModel>>,
}

impl ContractionReadModelProjector {
    pub fn create(repository: Box<dyn RepositoryTrait<ContractionReadModel>>) -> Self {
        Self {
            name: "ContractionReadModelProjector".to_string(),
            repository,
        }
    }

    fn project_event(
        &self,
        mut contractions: Vec<ContractionReadModel>,
        envelope: &EventEnvelope<LabourEvent>,
    ) -> Vec<ContractionReadModel> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        contractions
    }
}

#[async_trait(?Send)]
impl Projector<LabourEvent> for ContractionReadModelProjector {
    fn name(&self) -> &str {
        &self.name
    }

    async fn project_batch(&self, events: &[EventEnvelope<LabourEvent>]) -> Result<()> {
        if events.is_empty() {
            return Ok(());
        }

        Ok(())
    }
}
