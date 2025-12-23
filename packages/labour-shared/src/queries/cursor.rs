use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Cursor {
    pub id: Uuid,
    pub updated_at: String,
}
