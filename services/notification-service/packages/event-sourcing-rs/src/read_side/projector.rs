use anyhow::Result;
use async_trait::async_trait;

use crate::EventEnvelope;

#[async_trait(?Send)]
pub trait Projector<E> {
    async fn project_batch(&self, events: &[EventEnvelope<E>]) -> Result<()>;

    fn name(&self) -> &str;
}
