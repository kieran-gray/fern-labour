use anyhow::Result;
use uuid::Uuid;

use crate::DecodedCursor;

pub trait SyncRepositoryTrait<T> {
    fn get_by_id(&self, id: Uuid) -> Result<T>;
    fn get(&self, limit: usize, cursor: Option<DecodedCursor>) -> Result<Vec<T>>;
    fn upsert(&self, value: &T) -> Result<()>;
    fn delete(&self, id: Uuid) -> Result<()>;
    fn overwrite(&self, value: &T) -> Result<()>;
}
