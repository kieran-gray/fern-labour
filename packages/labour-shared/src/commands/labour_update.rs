use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::value_objects::LabourUpdateType;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum LabourUpdateCommand {
    PostLabourUpdate {
        labour_id: Uuid,
        labour_update_type: LabourUpdateType,
        message: String,
    },

    UpdateLabourUpdateMessage {
        labour_id: Uuid,
        labour_update_id: Uuid,
        message: String,
    },

    UpdateLabourUpdateType {
        labour_id: Uuid,
        labour_update_id: Uuid,
        labour_update_type: LabourUpdateType,
    },

    DeleteLabourUpdate {
        labour_id: Uuid,
        labour_update_id: Uuid,
    },
}

impl LabourUpdateCommand {
    pub fn labour_id(&self) -> Uuid {
        match self {
            LabourUpdateCommand::PostLabourUpdate { labour_id, .. } => *labour_id,
            LabourUpdateCommand::UpdateLabourUpdateMessage { labour_id, .. } => *labour_id,
            LabourUpdateCommand::UpdateLabourUpdateType { labour_id, .. } => *labour_id,
            LabourUpdateCommand::DeleteLabourUpdate { labour_id, .. } => *labour_id,
        }
    }
}
