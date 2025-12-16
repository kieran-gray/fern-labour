use std::str::FromStr;

use anyhow::{Result, anyhow};
use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::Cursor;
use fern_labour_labour_shared::value_objects::subscriber::status::SubscriberStatus;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SubscriptionStatusReadModel {
    pub subscription_id: Uuid,
    pub labour_id: Uuid,
    pub subscriber_id: String,
    pub status: SubscriberStatus,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl SubscriptionStatusReadModel {
    pub fn new(
        labour_id: Uuid,
        subscription_id: Uuid,
        subscriber_id: String,
        status: SubscriberStatus,
        created_at: DateTime<Utc>,
    ) -> Self {
        Self {
            labour_id,
            subscription_id,
            subscriber_id,
            status,
            created_at,
            updated_at: created_at,
        }
    }
}

impl Cursor for SubscriptionStatusReadModel {
    fn id(&self) -> Uuid {
        self.subscription_id
    }

    fn updated_at(&self) -> DateTime<Utc> {
        self.updated_at
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SubscriptionStatusRow {
    pub subscription_id: String,
    pub labour_id: String,
    pub subscriber_id: String,
    pub status: String,
    pub created_at: String,
    pub updated_at: String,
}

impl SubscriptionStatusRow {
    pub fn into_read_model(self) -> Result<SubscriptionStatusReadModel> {
        Ok(SubscriptionStatusReadModel {
            subscription_id: Uuid::parse_str(&self.subscription_id)
                .map_err(|e| anyhow!("Invalid subscription_id UUID: {}", e))?,
            labour_id: Uuid::parse_str(&self.labour_id)
                .map_err(|e| anyhow!("Invalid labour_id UUID: {}", e))?,
            subscriber_id: self.subscriber_id,
            status: Self::parse_subscriber_status(&self.status)?,
            created_at: Self::parse_timestamp(&self.created_at)?,
            updated_at: Self::parse_timestamp(&self.updated_at)?,
        })
    }

    pub fn from_read_model(model: &SubscriptionStatusReadModel) -> Result<Self> {
        Ok(Self {
            subscription_id: model.subscription_id.to_string(),
            labour_id: model.labour_id.to_string(),
            subscriber_id: model.subscriber_id.clone(),
            status: model.status.to_string(),
            created_at: model.created_at.to_rfc3339(),
            updated_at: model.updated_at.to_rfc3339(),
        })
    }

    fn parse_subscriber_status(status: &str) -> Result<SubscriberStatus> {
        let status =
            SubscriberStatus::from_str(status).map_err(|e| anyhow!("Invalid status: {}", e))?;
        Ok(status)
    }

    fn parse_timestamp(timestamp: &str) -> Result<DateTime<Utc>> {
        let datetime = DateTime::parse_from_rfc3339(timestamp)
            .map_err(|e| anyhow!("Invalid timestamp: {}", e))?
            .with_timezone(&Utc);
        Ok(datetime)
    }
}
