use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct PlanLabour {
    pub labour_id: Uuid,
    pub mother_id: String,
    pub mother_name: String,
    pub first_labour: bool,
    pub due_date: DateTime<Utc>,
    pub labour_name: Option<String>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct UpdateLabourPlan {
    pub labour_id: Uuid,
    pub first_labour: bool,
    pub due_date: DateTime<Utc>,
    pub labour_name: Option<String>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct BeginLabour {
    pub labour_id: Uuid,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct CompleteLabour {
    pub labour_id: Uuid,
    pub notes: Option<String>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct SendLabourInvite {
    pub labour_id: Uuid,
    pub invite_email: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct DeleteLabour {
    pub labour_id: Uuid,
}
