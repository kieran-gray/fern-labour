use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Deserialize)]
pub struct PaginatedQuery {
    pub limit: Option<usize>,
    pub cursor: Option<String>,
}

#[derive(Clone, Debug)]
pub struct DecodedCursor {
    pub last_updated_at: DateTime<Utc>,
    pub last_id: Uuid,
}

pub trait Cursor {
    fn id(&self) -> Uuid;
    fn updated_at(&self) -> DateTime<Utc>;
}

#[derive(Serialize)]
pub struct PaginatedResponse<T> {
    pub data: Vec<T>,
    pub next_cursor: Option<String>,
    pub has_more: bool,
}
