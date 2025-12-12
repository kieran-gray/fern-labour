use anyhow::Result;
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::{DecodedCursor, SyncRepositoryTrait};
use uuid::Uuid;

use crate::durable_object::read_side::read_models::{
    contractions::ContractionReadModel
};

#[async_trait(?Send)]
pub trait ContractionReadModelQueryHandler {
    fn get(&self, limit: usize, cursor: Option<DecodedCursor>)
    -> Result<Vec<ContractionReadModel>>;
    fn get_by_id(&self, id: Uuid) -> Result<ContractionReadModel>;
}

pub struct ContractionReadModelQuery {
    repository: Box<dyn SyncRepositoryTrait<ContractionReadModel>>,
}

impl ContractionReadModelQuery {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<ContractionReadModel>>) -> Self {
        Self { repository }
    }
}

impl ContractionReadModelQueryHandler for ContractionReadModelQuery {
    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<ContractionReadModel>> {
        let contractions = self.repository.get(limit, cursor)?;
        Ok(contractions)
    }
    
    fn get_by_id(&self, id:Uuid) -> Result<ContractionReadModel> {
        let contraction = self.repository.get_by_id(id)?;
        Ok(contraction)
    }
}
