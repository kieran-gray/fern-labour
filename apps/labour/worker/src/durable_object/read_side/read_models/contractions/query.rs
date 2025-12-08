use anyhow::Result;
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::SingleItemRepositoryTrait;

use crate::durable_object::read_side::read_models::labour::read_model::LabourReadModel;

#[async_trait(?Send)]
pub trait LabourReadModelQueryHandler {
    async fn get(&self) -> Result<LabourReadModel>;
}

pub struct LabourReadModelQuery {
    repository: Box<dyn SingleItemRepositoryTrait<LabourReadModel>>,
}

impl LabourReadModelQuery {
    pub fn create(repository: Box<dyn SingleItemRepositoryTrait<LabourReadModel>>) -> Self {
        Self { repository }
    }
}

#[async_trait(?Send)]
impl LabourReadModelQueryHandler for LabourReadModelQuery {
    async fn get(&self) -> Result<LabourReadModel> {
        let labour = self.repository.get().await?;

        Ok(labour)
    }
}
