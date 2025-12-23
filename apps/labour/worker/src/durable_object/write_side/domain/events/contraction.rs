use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::{Event, impl_labour_event};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct ContractionStarted {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
    pub start_time: DateTime<Utc>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct ContractionEnded {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
    pub end_time: DateTime<Utc>,
    pub intensity: u8,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct ContractionUpdated {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
    pub start_time: Option<DateTime<Utc>>,
    pub end_time: Option<DateTime<Utc>>,
    pub intensity: Option<u8>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct ContractionDeleted {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
}

impl_labour_event!(ContractionStarted, labour_id);
impl_labour_event!(ContractionEnded, labour_id);
impl_labour_event!(ContractionUpdated, labour_id);
impl_labour_event!(ContractionDeleted, labour_id);
