use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::value_objects::LabourUpdateType;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum LabourUpdateCommand {
    #[serde(rename = "PostLabourUpdate")]
    PostLabourUpdate {
        labour_id: Uuid,
        labour_update_type: LabourUpdateType,
        message: String,
    },

    #[serde(rename = "UpdateLabourUpdateMessage")]
    UpdateLabourUpdateMessage {
        labour_id: Uuid,
        labour_update_id: Uuid,
        message: String,
    },

    #[serde(rename = "UpdateLabourUpdateType")]
    UpdateLabourUpdateType {
        labour_id: Uuid,
        labour_update_id: Uuid,
        labour_update_type: LabourUpdateType,
    },

    #[serde(rename = "DeleteLabourUpdate")]
    DeleteLabourUpdate {
        labour_id: Uuid,
        labour_update_id: Uuid,
    },
}

impl LabourUpdateCommand {
    pub fn labour_id(&self) -> Option<Uuid> {
        match self {
            LabourUpdateCommand::PostLabourUpdate { labour_id, .. } => Some(*labour_id),
            LabourUpdateCommand::UpdateLabourUpdateMessage { labour_id, .. } => Some(*labour_id),
            LabourUpdateCommand::UpdateLabourUpdateType { labour_id, .. } => Some(*labour_id),
            LabourUpdateCommand::DeleteLabourUpdate { labour_id, .. } => Some(*labour_id),
        }
    }
}
