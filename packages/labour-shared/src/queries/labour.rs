use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum LabourQuery {
    #[serde(rename = "GetLabour")]
    GetLabour { labour_id: Uuid },
}

impl LabourQuery {
    pub fn labour_id(&self) -> Uuid {
        match self {
            LabourQuery::GetLabour { labour_id } => *labour_id,
        }
    }
}
