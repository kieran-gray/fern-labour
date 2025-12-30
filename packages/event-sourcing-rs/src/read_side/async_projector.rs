use std::rc::Rc;

use anyhow::Result;
use async_trait::async_trait;
use serde::{Deserialize, Serialize};

use crate::{CacheTrait, EventEnvelope};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CachedReadModelState<T> {
    pub sequence: i64,
    pub model: Option<T>,
}

impl<T> CachedReadModelState<T> {
    pub fn new(sequence: i64, model: Option<T>) -> Self {
        Self { sequence, model }
    }

    pub fn empty() -> Self {
        Self {
            sequence: 0,
            model: None,
        }
    }
}

#[async_trait(?Send)]
pub trait AsyncProjector<E> {
    async fn project_batch(&self, events: &[EventEnvelope<E>]) -> Result<()>;

    fn name(&self) -> &str;
}

#[async_trait(?Send)]
pub trait IncrementalAsyncProjector<E> {
    fn name(&self) -> &str;

    fn get_cached_sequence(&self, cache: &Rc<dyn CacheTrait>) -> i64;

    async fn process(
        &self,
        cache: &Rc<dyn CacheTrait>,
        events: &[EventEnvelope<E>],
        max_sequence: i64,
    ) -> Result<()>;
}
