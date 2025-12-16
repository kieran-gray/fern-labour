use anyhow::Result;
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::DecodedCursor;
use uuid::Uuid;

use crate::durable_object::read_side::read_models::subscriptions::{
    SubscriptionReadModel, sync_repository::SubscriptionRepositoryTrait,
};

#[async_trait(?Send)]
pub trait SubscriptionReadModelQueryHandler {
    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<SubscriptionReadModel>>;
    fn get_by_id(&self, id: Uuid) -> Result<SubscriptionReadModel>;
    fn get_user_subscription(&self, user_id: String) -> Result<SubscriptionReadModel>;
}

pub struct SubscriptionReadModelQuery {
    repository: Box<dyn SubscriptionRepositoryTrait>,
}

impl SubscriptionReadModelQuery {
    pub fn create(repository: Box<dyn SubscriptionRepositoryTrait>) -> Self {
        Self { repository }
    }
}

impl SubscriptionReadModelQueryHandler for SubscriptionReadModelQuery {
    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<SubscriptionReadModel>> {
        let subscriptions = self.repository.get(limit, cursor)?;
        Ok(subscriptions)
    }

    fn get_by_id(&self, id: Uuid) -> Result<SubscriptionReadModel> {
        let subscription = self.repository.get_by_id(id)?;
        Ok(subscription)
    }

    fn get_user_subscription(&self, user_id: String) -> Result<SubscriptionReadModel> {
        let subscription = self.repository.get_by_subscriber_id(&user_id)?;
        Ok(subscription)
    }
}
