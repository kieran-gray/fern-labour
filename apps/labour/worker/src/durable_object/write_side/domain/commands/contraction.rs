use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StartContraction {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
    pub start_time: DateTime<Utc>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct EndContraction {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
    pub end_time: DateTime<Utc>,
    pub intensity: u8,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct UpdateContraction {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
    pub start_time: Option<DateTime<Utc>>,
    pub end_time: Option<DateTime<Utc>>,
    pub intensity: Option<u8>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct DeleteContraction {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
}
