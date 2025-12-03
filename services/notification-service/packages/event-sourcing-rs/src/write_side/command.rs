use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CommandMetadata {
    pub idempotency_key: Uuid,
    pub command_id: Uuid,
    pub aggregate_id: Uuid,
    pub correlation_id: Uuid,
    pub causation_id: Uuid,
    pub user_id: String,
    pub timestamp: DateTime<Utc>,
}

impl CommandMetadata {
    pub fn new(
        aggregate_id: Uuid,
        correlation_id: Uuid,
        causation_id: Uuid,
        user_id: String,
        timestamp: DateTime<Utc>,
    ) -> Self {
        Self {
            idempotency_key: Uuid::now_v7(),
            command_id: Uuid::now_v7(),
            aggregate_id,
            correlation_id,
            causation_id,
            user_id,
            timestamp,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CommandEnvelope<C> {
    pub metadata: CommandMetadata,
    pub command: C,
}

impl<C> CommandEnvelope<C> {
    pub fn new(metadata: CommandMetadata, command: C) -> Self {
        Self { metadata, command }
    }

    pub fn enrich(
        command: C,
        aggregate_id: Uuid,
        correlation_id: Uuid,
        causation_id: Uuid,
        user_id: String,
        timestamp: DateTime<Utc>,
    ) -> Self {
        Self {
            metadata: CommandMetadata::new(
                aggregate_id,
                correlation_id,
                causation_id,
                user_id,
                timestamp,
            ),
            command,
        }
    }
}
