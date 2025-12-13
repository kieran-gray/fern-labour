use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::{ContractionQuery, LabourQuery, LabourUpdateQuery};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum ApiQuery {
    #[serde(rename = "Labour")]
    Labour(LabourQuery),

    #[serde(rename = "Contraction")]
    Contraction(ContractionQuery),

    #[serde(rename = "LabourUpdate")]
    LabourUpdate(LabourUpdateQuery),
}

impl ApiQuery {
    pub fn labour_id(&self) -> Uuid {
        match self {
            Self::Labour(query) => query.labour_id(),
            Self::Contraction(query) => query.labour_id(),
            Self::LabourUpdate(query) => query.labour_id(),
        }
    }
}
