use anyhow::{Result, anyhow};
use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::Cursor;
use fern_labour_labour_shared::value_objects::contraction::duration::Duration;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContractionReadModel {
    pub labour_id: Uuid,
    pub contraction_id: Uuid,
    pub duration: Duration,
    pub intensity: Option<u8>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl ContractionReadModel {
    pub fn new(
        labour_id: Uuid,
        contraction_id: Uuid,
        duration: Duration,
        intensity: Option<u8>,
        created_at: DateTime<Utc>,
    ) -> Self {
        Self {
            labour_id,
            contraction_id,
            duration,
            intensity,
            created_at,
            updated_at: created_at,
        }
    }
}

impl Cursor for ContractionReadModel {
    fn id(&self) -> Uuid {
        self.labour_id
    }

    fn updated_at(&self) -> DateTime<Utc> {
        self.updated_at
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ContractionRow {
    pub labour_id: String,
    pub contraction_id: String,
    pub duration: String,
    pub intensity: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl ContractionRow {
    pub fn into_read_model(self) -> Result<ContractionReadModel> {
        Ok(ContractionReadModel {
            labour_id: Uuid::parse_str(&self.labour_id)
                .map_err(|e| anyhow!("Invalid labour_id UUID: {}", e))?,
            contraction_id: Uuid::parse_str(&self.contraction_id)
                .map_err(|e| anyhow!("Invalid contraction_id UUID: {}", e))?,
            duration: Self::parse_duration(&self.duration)?,
            intensity: Self::parse_optional_intensity(self.intensity)?,
            created_at: Self::parse_timestamp(&self.created_at)?,
            updated_at: Self::parse_timestamp(&self.updated_at)?,
        })
    }

    pub fn from_read_model(model: &ContractionReadModel) -> Result<Self> {
        Ok(Self {
            labour_id: model.labour_id.to_string(),
            contraction_id: model.contraction_id.to_string(),
            duration: Self::serialize_duration(&model.duration)?,
            intensity: model.intensity.map(|i| i.to_string()),
            created_at: model.created_at.to_rfc3339(),
            updated_at: model.updated_at.to_rfc3339(),
        })
    }

    fn parse_duration(duration_str: &str) -> Result<Duration> {
        serde_json::from_str::<Duration>(duration_str)
            .map_err(|e| anyhow!("Invalid duration JSON: {}", e))
    }

    fn serialize_duration(duration: &Duration) -> Result<String> {
        serde_json::to_string(duration).map_err(|e| anyhow!("Failed to serialize duration: {}", e))
    }

    fn parse_optional_intensity(intensity_str: Option<String>) -> Result<Option<u8>> {
        match intensity_str {
            Some(s) => {
                let value = s
                    .parse::<u8>()
                    .map_err(|e| anyhow!("Invalid intensity value '{}': {}", s, e))?;
                Ok(Some(value))
            }
            None => Ok(None),
        }
    }

    fn parse_timestamp(timestamp: &str) -> Result<DateTime<Utc>> {
        let datetime = DateTime::parse_from_rfc3339(timestamp)
            .map_err(|e| anyhow!("Invalid timestamp: {}", e))?
            .with_timezone(&Utc);
        Ok(datetime)
    }
}
