use anyhow::Result;
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::{DecodedCursor, SyncRepositoryTrait};
use uuid::Uuid;

use crate::durable_object::read_side::read_models::subscriptions::SubscriptionReadModel;

#[async_trait(?Send)]
pub trait SubscriptionReadModelQueryHandler {
    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<SubscriptionReadModel>>;
    fn get_by_id(&self, id: Uuid) -> Result<SubscriptionReadModel>;
}

pub struct SubscriptionReadModelQuery {
    repository: Box<dyn SyncRepositoryTrait<SubscriptionReadModel>>,
}

impl SubscriptionReadModelQuery {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<SubscriptionReadModel>>) -> Self {
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
}
