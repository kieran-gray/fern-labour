use anyhow::Result;
use async_trait::async_trait;
use uuid::Uuid;

use crate::durable_object::read_side::read_models::labour_status::{
    LabourStatusReadModel, async_repository::LabourStatusRepositoryTrait,
};

#[async_trait(?Send)]
pub trait LabourStatusReadModelQueryHandler {
    async fn get_by_user_id(&self, user_id: String) -> Result<Vec<LabourStatusReadModel>>;
    async fn get_active(&self, user_id: String) -> Result<Option<LabourStatusReadModel>>;
    async fn get_by_ids(&self, labour_ids: Vec<Uuid>) -> Result<Vec<LabourStatusReadModel>>;
}

pub struct LabourStatusReadModelQuery {
    repository: Box<dyn LabourStatusRepositoryTrait>,
}

impl LabourStatusReadModelQuery {
    pub fn create(repository: Box<dyn LabourStatusRepositoryTrait>) -> Self {
        Self { repository }
    }
}

#[async_trait(?Send)]
impl LabourStatusReadModelQueryHandler for LabourStatusReadModelQuery {
    async fn get_by_user_id(&self, user_id: String) -> Result<Vec<LabourStatusReadModel>> {
        self.repository.get_by_user_id(user_id, 20, None).await
    }

    async fn get_active(&self, user_id: String) -> Result<Option<LabourStatusReadModel>> {
        self.repository.get_active_labour(user_id).await
    }

    async fn get_by_ids(&self, labour_ids: Vec<Uuid>) -> Result<Vec<LabourStatusReadModel>> {
        self.repository.get_by_ids(labour_ids).await
    }
}
