use anyhow::Result;

use crate::durable_object::read_side::read_models::subscription_token::{
    SubscriptionTokenReadModel, sync_repository::SubscriptionTokenRepositoryTrait,
};

pub trait SubscriptionTokenQueryHandler {
    fn get(&self) -> Result<Option<SubscriptionTokenReadModel>>;
}

pub struct SubscriptionTokenQuery {
    repository: Box<dyn SubscriptionTokenRepositoryTrait>,
}

impl SubscriptionTokenQuery {
    pub fn create(repository: Box<dyn SubscriptionTokenRepositoryTrait>) -> Self {
        Self { repository }
    }
}

impl SubscriptionTokenQueryHandler for SubscriptionTokenQuery {
    fn get(&self) -> Result<Option<SubscriptionTokenReadModel>> {
        self.repository.get_token()
    }
}
