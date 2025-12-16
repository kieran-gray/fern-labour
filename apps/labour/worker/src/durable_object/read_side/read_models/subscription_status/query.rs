use anyhow::Result;
use async_trait::async_trait;

use crate::durable_object::read_side::read_models::subscription_status::{
    SubscriptionStatusReadModel, async_repository::SubscriptionStatusRepositoryTrait,
};

#[async_trait(?Send)]
pub trait SubscriptionStatusReadModelQueryHandler {
    async fn get_by_user_id(&self, user_id: String) -> Result<Vec<SubscriptionStatusReadModel>>;
}

pub struct SubscriptionStatusReadModelQuery {
    repository: Box<dyn SubscriptionStatusRepositoryTrait>,
}

impl SubscriptionStatusReadModelQuery {
    pub fn create(repository: Box<dyn SubscriptionStatusRepositoryTrait>) -> Self {
        Self { repository }
    }
}

#[async_trait(?Send)]
impl SubscriptionStatusReadModelQueryHandler for SubscriptionStatusReadModelQuery {
    async fn get_by_user_id(&self, user_id: String) -> Result<Vec<SubscriptionStatusReadModel>> {
        self.repository.get_by_user_id(user_id, 20, None).await
    }
}
