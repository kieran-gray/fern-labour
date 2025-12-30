use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::{Event, impl_event};
use fern_labour_labour_shared::value_objects::LabourPhase;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourPlanned {
    pub labour_id: Uuid,
    pub mother_id: String,
    pub mother_name: String, // TODO: Decide if we are removing this
    pub first_labour: bool,
    pub due_date: DateTime<Utc>,
    pub labour_name: Option<String>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourPlanUpdated {
    pub labour_id: Uuid,
    pub first_labour: bool,
    pub due_date: DateTime<Utc>,
    pub labour_name: Option<String>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourBegun {
    pub labour_id: Uuid,
    pub start_time: DateTime<Utc>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourCompleted {
    pub labour_id: Uuid,
    pub notes: Option<String>,
    pub end_time: DateTime<Utc>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourInviteSent {
    pub labour_id: Uuid,
    pub invite_email: String,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourDeleted {
    pub labour_id: Uuid,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct LabourPhaseChanged {
    pub labour_id: Uuid,
    pub labour_phase: LabourPhase,
}

impl_event!(LabourPlanned, labour_id);
impl_event!(LabourPlanUpdated, labour_id);
impl_event!(LabourBegun, labour_id);
impl_event!(LabourCompleted, labour_id);
impl_event!(LabourInviteSent, labour_id);
impl_event!(LabourDeleted, labour_id);
impl_event!(LabourPhaseChanged, labour_id);
