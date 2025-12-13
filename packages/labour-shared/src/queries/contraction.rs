use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Cursor {
    pub id: Uuid,
    pub updated_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum ContractionQuery {
    #[serde(rename = "GetContractions")]
    GetContractions {
        labour_id: Uuid,
        limit: usize,
        cursor: Option<Cursor>,
    },

    #[serde(rename = "GetContractionById")]
    GetContractionById {
        labour_id: Uuid,
        contraction_id: Uuid,
    },
}

impl ContractionQuery {
    pub fn labour_id(&self) -> Uuid {
        match self {
            ContractionQuery::GetContractions { labour_id, .. } => *labour_id,
            ContractionQuery::GetContractionById { labour_id, .. } => *labour_id,
        }
    }
}
