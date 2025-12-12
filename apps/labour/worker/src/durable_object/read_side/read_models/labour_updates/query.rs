use anyhow::Result;
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::{DecodedCursor, SyncRepositoryTrait};
use uuid::Uuid;

use crate::durable_object::read_side::read_models::labour_updates::LabourUpdateReadModel;

#[async_trait(?Send)]
pub trait LabourUpdateReadModelQueryHandler {
    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<LabourUpdateReadModel>>;
    fn get_by_id(&self, id: Uuid) -> Result<LabourUpdateReadModel>;
}

pub struct LabourUpdateReadModelQuery {
    repository: Box<dyn SyncRepositoryTrait<LabourUpdateReadModel>>,
}

impl LabourUpdateReadModelQuery {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<LabourUpdateReadModel>>) -> Self {
        Self { repository }
    }
}

impl LabourUpdateReadModelQueryHandler for LabourUpdateReadModelQuery {
    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<LabourUpdateReadModel>> {
        let labour_updates = self.repository.get(limit, cursor)?;
        Ok(labour_updates)
    }

    fn get_by_id(&self, id: Uuid) -> Result<LabourUpdateReadModel> {
        let labour_update = self.repository.get_by_id(id)?;
        Ok(labour_update)
    }
}
