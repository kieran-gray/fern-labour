use fern_labour_labour_shared::value_objects::LabourUpdateType;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct PostLabourUpdate {
    pub labour_id: Uuid,
    pub labour_update_type: LabourUpdateType,
    pub message: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct PostApplicationLabourUpdate {
    pub labour_id: Uuid,
    pub message: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct UpdateLabourUpdateMessage {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
    pub message: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct UpdateLabourUpdateType {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
    pub labour_update_type: LabourUpdateType,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct DeleteLabourUpdate {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
}
