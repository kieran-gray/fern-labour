use serde::{Deserialize, Serialize};
use uuid::Uuid;

use super::contraction::Cursor;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum LabourUpdateQuery {
    #[serde(rename = "GetLabourUpdates")]
    GetLabourUpdates {
        labour_id: Uuid,
        limit: usize,
        cursor: Option<Cursor>,
    },

    #[serde(rename = "GetLabourUpdateById")]
    GetLabourUpdateById {
        labour_id: Uuid,
        labour_update_id: Uuid,
    },
}

impl LabourUpdateQuery {
    pub fn labour_id(&self) -> Uuid {
        match self {
            LabourUpdateQuery::GetLabourUpdates { labour_id, .. } => *labour_id,
            LabourUpdateQuery::GetLabourUpdateById { labour_id, .. } => *labour_id,
        }
    }
}
