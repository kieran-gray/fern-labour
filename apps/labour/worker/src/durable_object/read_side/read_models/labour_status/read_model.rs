use std::str::FromStr;

use anyhow::{Result, anyhow};
use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::Cursor;
use fern_labour_labour_shared::value_objects::LabourPhase;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LabourStatusReadModel {
    pub labour_id: Uuid,
    pub birthing_person_id: String,
    pub current_phase: LabourPhase,
    pub labour_name: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl LabourStatusReadModel {
    pub fn new(
        labour_id: Uuid,
        birthing_person_id: String,
        labour_name: Option<String>,
        created_at: DateTime<Utc>,
    ) -> Self {
        Self {
            labour_id,
            birthing_person_id,
            current_phase: LabourPhase::PLANNED,
            labour_name,
            created_at,
            updated_at: created_at,
        }
    }
}

impl Cursor for LabourStatusReadModel {
    fn id(&self) -> Uuid {
        self.labour_id
    }

    fn updated_at(&self) -> DateTime<Utc> {
        self.updated_at
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct LabourStatusRow {
    pub labour_id: String,
    pub birthing_person_id: String,
    pub current_phase: String,
    pub labour_name: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl LabourStatusRow {
    pub fn into_read_model(self) -> Result<LabourStatusReadModel> {
        Ok(LabourStatusReadModel {
            labour_id: Uuid::parse_str(&self.labour_id)
                .map_err(|e| anyhow!("Invalid labour_id UUID: {}", e))?,
            birthing_person_id: self.birthing_person_id,
            current_phase: Self::parse_labour_phase(&self.current_phase)?,
            labour_name: self.labour_name,
            created_at: Self::parse_timestamp(&self.created_at)?,
            updated_at: Self::parse_timestamp(&self.updated_at)?,
        })
    }

    pub fn from_read_model(model: &LabourStatusReadModel) -> Result<Self> {
        Ok(Self {
            labour_id: model.labour_id.to_string(),
            birthing_person_id: model.birthing_person_id.clone(),
            current_phase: model.current_phase.to_string(),
            labour_name: model.labour_name.clone(),
            created_at: model.created_at.to_rfc3339(),
            updated_at: model.updated_at.to_rfc3339(),
        })
    }

    fn parse_labour_phase(phase: &str) -> Result<LabourPhase> {
        let phase =
            LabourPhase::from_str(phase).map_err(|e| anyhow!("Invalid labour_phase: {}", e))?;
        Ok(phase)
    }

    fn parse_timestamp(timestamp: &str) -> Result<DateTime<Utc>> {
        let datetime = DateTime::parse_from_rfc3339(timestamp)
            .map_err(|e| anyhow!("Invalid timestamp: {}", e))?
            .with_timezone(&Utc);
        Ok(datetime)
    }
}
