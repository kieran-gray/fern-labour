use anyhow::Result;

use crate::EventEnvelope;

pub trait SyncProjector<E> {
    fn project_batch(&self, events: &[EventEnvelope<E>]) -> Result<()>;

    fn name(&self) -> &str;
}
