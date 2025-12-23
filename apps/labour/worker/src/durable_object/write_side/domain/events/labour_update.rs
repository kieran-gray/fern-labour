use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::{Event, impl_labour_event};
use fern_labour_labour_shared::value_objects::LabourUpdateType;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourUpdatePosted {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
    pub labour_update_type: LabourUpdateType,
    pub message: String,
    pub application_generated: bool,
    pub sent_time: DateTime<Utc>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourUpdateMessageUpdated {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
    pub message: String,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourUpdateTypeUpdated {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
    pub labour_update_type: LabourUpdateType,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourUpdateDeleted {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
}

impl_labour_event!(LabourUpdatePosted, labour_id);
impl_labour_event!(LabourUpdateMessageUpdated, labour_id);
impl_labour_event!(LabourUpdateTypeUpdated, labour_id);
impl_labour_event!(LabourUpdateDeleted, labour_id);
