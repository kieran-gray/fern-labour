use anyhow::Result;
use async_trait::async_trait;

#[async_trait(?Send)]
pub trait SingleItemRepositoryTrait<T> {
    async fn get(&self) -> Result<T>;
    async fn delete(&self) -> Result<()>;
    async fn overwrite(&self, value: &T) -> Result<()>;
}
