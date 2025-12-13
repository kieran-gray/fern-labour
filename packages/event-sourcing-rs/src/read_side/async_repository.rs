use anyhow::Result;
use async_trait::async_trait;
use uuid::Uuid;

use crate::DecodedCursor;

#[async_trait(?Send)]
pub trait AsyncRepositoryTrait<T> {
    async fn get_by_id(&self, id: Uuid) -> Result<T>;
    async fn get(&self, limit: usize, cursor: Option<DecodedCursor>) -> Result<Vec<T>>;
    async fn upsert(&self, value: &T) -> Result<()>;
    async fn delete(&self, id: Uuid) -> Result<()>;
    async fn overwrite(&self, value: &T) -> Result<()>;
}

#[async_trait(?Send)]
pub trait AsyncRepositoryUserTrait<T> {
    async fn get_by_user_id(
        &self,
        user_id: String,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<T>>;
}
