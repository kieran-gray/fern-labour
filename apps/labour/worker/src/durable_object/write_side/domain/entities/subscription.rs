use fern_labour_labour_shared::value_objects::{
    SubscriberAccessLevel, SubscriberContactMethod, SubscriberRole,
    subscriber::status::SubscriberStatus,
};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Subscription {
    id: Uuid,
    labour_id: Uuid,
    subscriber_id: String,
    role: SubscriberRole,
    status: SubscriberStatus,
    access_level: SubscriberAccessLevel,
    contact_methods: Vec<SubscriberContactMethod>,
}

impl Subscription {
    pub fn create(subscription_id: Uuid, labour_id: Uuid, subscriber_id: String) -> Self {
        Self {
            id: subscription_id,
            labour_id,
            subscriber_id,
            role: SubscriberRole::FRIENDS_AND_FAMILY,
            status: SubscriberStatus::REQUESTED,
            access_level: SubscriberAccessLevel::BASIC,
            contact_methods: vec![],
        }
    }

    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn subscriber_id(&self) -> &str {
        &self.subscriber_id
    }

    pub fn status(&self) -> &SubscriberStatus {
        &self.status
    }

    pub fn access_level(&self) -> &SubscriberAccessLevel {
        &self.access_level
    }

    pub fn role(&self) -> &SubscriberRole {
        &self.role
    }

    pub fn request(&mut self) {
        self.status = SubscriberStatus::REQUESTED
    }

    pub fn approve(&mut self) {
        self.status = SubscriberStatus::SUBSCRIBED;
    }

    pub fn unsubscribe(&mut self) {
        self.status = SubscriberStatus::UNSUBSCRIBED;
    }

    pub fn remove(&mut self) {
        self.status = SubscriberStatus::REMOVED;
    }

    pub fn block(&mut self) {
        self.status = SubscriberStatus::BLOCKED;
    }

    pub fn unblock(&mut self) {
        self.status = SubscriberStatus::REMOVED;
    }

    pub fn update_notification_methods(&mut self, contact_methods: Vec<SubscriberContactMethod>) {
        self.contact_methods = contact_methods;
    }

    pub fn update_access_level(&mut self, access_level: SubscriberAccessLevel) {
        self.access_level = access_level;
    }

    pub fn update_role(&mut self, role: SubscriberRole) {
        self.role = role;
    }
}
