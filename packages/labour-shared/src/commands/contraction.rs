use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum ContractionCommand {
    #[serde(rename = "StartContraction")]
    StartContraction {
        labour_id: Uuid,
        start_time: DateTime<Utc>,
    },

    #[serde(rename = "EndContraction")]
    EndContraction {
        labour_id: Uuid,
        end_time: DateTime<Utc>,
        intensity: u8,
    },

    #[serde(rename = "UpdateContraction")]
    UpdateContraction {
        labour_id: Uuid,
        contraction_id: Uuid,
        start_time: Option<DateTime<Utc>>,
        end_time: Option<DateTime<Utc>>,
        intensity: Option<u8>,
    },

    #[serde(rename = "DeleteContraction")]
    DeleteContraction {
        labour_id: Uuid,
        contraction_id: Uuid,
    },
}

impl ContractionCommand {
    pub fn labour_id(&self) -> Option<Uuid> {
        match self {
            ContractionCommand::StartContraction { labour_id, .. } => Some(*labour_id),
            ContractionCommand::EndContraction { labour_id, .. } => Some(*labour_id),
            ContractionCommand::UpdateContraction { labour_id, .. } => Some(*labour_id),
            ContractionCommand::DeleteContraction { labour_id, .. } => Some(*labour_id),
        }
    }
}
