use anyhow::{Result, anyhow};
use fern_labour_event_sourcing_rs::SyncRepositoryTrait;

use crate::durable_object::read_side::read_models::labour::read_model::LabourReadModel;

pub trait LabourReadModelQueryHandler {
    fn get(&self) -> Result<LabourReadModel>;
}

pub struct LabourReadModelQuery {
    repository: Box<dyn SyncRepositoryTrait<LabourReadModel>>,
}

impl LabourReadModelQuery {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<LabourReadModel>>) -> Self {
        Self { repository }
    }
}

impl LabourReadModelQueryHandler for LabourReadModelQuery {
    fn get(&self) -> Result<LabourReadModel> {
        match self.repository.get(1, None)?.into_iter().next() {
            Some(labour) => Ok(labour),
            None => Err(anyhow!("Labour not found")),
        }
    }
}
