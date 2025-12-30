use fern_labour_event_sourcing_rs::{Event, impl_event};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct SubscriptionTokenSet {
    pub labour_id: Uuid,
    pub mother_id: String,
    pub token: String,
}

impl_event!(SubscriptionTokenSet, labour_id);
