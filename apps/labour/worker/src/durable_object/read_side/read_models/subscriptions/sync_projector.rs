use anyhow::Result;
use async_trait::async_trait;
use fern_labour_labour_shared::value_objects::{
    SubscriberAccessLevel, SubscriberRole, subscriber::status::SubscriberStatus,
};

use fern_labour_event_sourcing_rs::{EventEnvelope, SyncProjector, SyncRepositoryTrait};

use crate::durable_object::{
    read_side::read_models::subscriptions::SubscriptionReadModel, write_side::domain::LabourEvent,
};

pub struct SubscriptionReadModelProjector {
    name: String,
    repository: Box<dyn SyncRepositoryTrait<SubscriptionReadModel>>,
}

impl SubscriptionReadModelProjector {
    pub fn create(repository: Box<dyn SyncRepositoryTrait<SubscriptionReadModel>>) -> Self {
        Self {
            name: "SubscriptionReadModelProjector".to_string(),
            repository,
        }
    }

    fn project_event(&self, envelope: &EventEnvelope<LabourEvent>) -> Result<()> {
        let event = &envelope.event;
        let metadata = &envelope.metadata;
        let timestamp = metadata.timestamp;

        match event {
            LabourEvent::SubscriberRequested {
                labour_id,
                subscriber_id,
                subscription_id,
            } => match self.repository.get_by_id(*subscription_id) {
                Ok(mut existing_subscription) => {
                    existing_subscription.status = SubscriberStatus::REQUESTED;
                    existing_subscription.updated_at = timestamp;
                    self.repository.upsert(&existing_subscription)
                }
                Err(_) => {
                    let subscription = SubscriptionReadModel::new(
                        *subscription_id,
                        *labour_id,
                        subscriber_id.clone(),
                        SubscriberRole::FRIENDS_AND_FAMILY,
                        SubscriberStatus::REQUESTED,
                        SubscriberAccessLevel::BASIC,
                        vec![],
                        timestamp,
                    );
                    self.repository.overwrite(&subscription)
                }
            },
            LabourEvent::SubscriberApproved {
                subscription_id, ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.status = SubscriberStatus::SUBSCRIBED;
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            LabourEvent::SubscriberUnsubscribed {
                subscription_id, ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.status = SubscriberStatus::UNSUBSCRIBED;
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            LabourEvent::SubscriberRemoved {
                subscription_id, ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.status = SubscriberStatus::REMOVED;
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            LabourEvent::SubscriberBlocked {
                subscription_id, ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.status = SubscriberStatus::BLOCKED;
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            LabourEvent::SubscriberUnblocked {
                subscription_id, ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.status = SubscriberStatus::REMOVED;
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            LabourEvent::SubscriberRoleUpdated {
                subscription_id,
                role,
                ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.role = role.clone();
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            LabourEvent::SubscriberAccessLevelUpdated {
                subscription_id,
                access_level,
                ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.access_level = access_level.clone();
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            LabourEvent::SubscriberNotificationMethodsUpdated {
                subscription_id,
                notification_methods,
                ..
            } => {
                let mut subscription = self
                    .repository
                    .get_by_id(*subscription_id)
                    .unwrap_or_else(|_| panic!("No subscription found with id: {subscription_id}"));
                subscription.contact_methods = notification_methods.clone();
                subscription.updated_at = timestamp;
                self.repository.upsert(&subscription)
            }
            _ => Ok(()),
        }
    }
}

#[async_trait(?Send)]
impl SyncProjector<LabourEvent> for SubscriptionReadModelProjector {
    fn name(&self) -> &str {
        &self.name
    }

    fn project_batch(&self, events: &[EventEnvelope<LabourEvent>]) -> Result<()> {
        if events.is_empty() {
            return Ok(());
        }

        events
            .iter()
            .try_for_each(|envelope| self.project_event(envelope))
    }
}
