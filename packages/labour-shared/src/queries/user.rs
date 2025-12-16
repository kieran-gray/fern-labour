use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum UserQuery {
    #[serde(rename = "GetUser")]
    GetUser { labour_id: Uuid, user_id: String },
    GetUsers { labour_id: Uuid }
}

impl UserQuery {
    pub fn labour_id(&self) -> Uuid {
        match self {
            UserQuery::GetUser { labour_id, .. } => *labour_id,
            UserQuery::GetUsers { labour_id } => *labour_id,
        }
    }
}
