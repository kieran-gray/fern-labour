use anyhow::{Context, Result};
use async_trait::async_trait;
use chrono::{DateTime, NaiveDateTime, Utc};
use serde::{Deserialize, Serialize, de::DeserializeOwned};

use crate::{Event, EventEnvelope, EventEnvelopeAdapter, EventMetadata};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoredEventRow {
    pub sequence: i64,
    pub aggregate_id: String,
    pub event_type: String,
    pub event_data: String,
    pub event_version: i64,
    pub created_at: String,
    pub user_id: String,
}

impl<E: Event + DeserializeOwned> EventEnvelopeAdapter<E> for StoredEventRow {
    fn to_envelope(&self) -> Result<EventEnvelope<E>> {
        let event: E =
            serde_json::from_str(&self.event_data).context("Failed to deserialize event")?;

        let timestamp = NaiveDateTime::parse_from_str(&self.created_at, "%Y-%m-%d %H:%M:%S")
            .context("Failed to parse timestamp")?
            .and_utc();

        Ok(EventEnvelope {
            metadata: EventMetadata {
                aggregate_id: event.aggregate_id(),
                sequence: self.sequence,
                event_version: self.event_version,
                timestamp,
                user_id: self.user_id.clone(),
            },
            event,
        })
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoredEvent {
    pub aggregate_id: String,
    pub event_type: String,
    pub event_data: String,
    pub event_version: i64,
}

#[derive(Debug, Clone)]
pub struct AppendResult {
    pub sequence: i64,
    pub timestamp: DateTime<Utc>,
}

#[async_trait(?Send)]
pub trait EventStoreTrait: Send + Sync {
    fn init_schema(&self) -> Result<()>;
    fn append(
        &self,
        aggregate_id: String,
        event: StoredEvent,
        user_id: String,
    ) -> Result<AppendResult>;
    fn load(&self) -> Result<Vec<StoredEventRow>>;
    fn events_since(&self, sequence: i64, limit: i64) -> Result<Vec<StoredEventRow>>;
    fn max_sequence(&self) -> Result<Option<i64>>;
}
