use std::str::FromStr;

use anyhow::{Result, anyhow};
use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::Cursor;
use fern_labour_labour_shared::value_objects::LabourPhase;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LabourReadModel {
    pub labour_id: Uuid,
    pub birthing_person_id: String,
    pub current_phase: LabourPhase,
    pub first_labour: bool,
    pub due_date: DateTime<Utc>,
    pub labour_name: Option<String>,
    pub start_time: Option<DateTime<Utc>>,
    pub end_time: Option<DateTime<Utc>>,
    pub notes: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl LabourReadModel {
    pub fn new(
        labour_id: Uuid,
        birthing_person_id: String,
        first_labour: bool,
        due_date: DateTime<Utc>,
        labour_name: Option<String>,
        created_at: DateTime<Utc>,
    ) -> Self {
        Self {
            labour_id,
            birthing_person_id,
            current_phase: LabourPhase::PLANNED,
            first_labour,
            due_date,
            labour_name,
            start_time: None,
            end_time: None,
            notes: None,
            created_at,
            updated_at: created_at,
        }
    }
}

impl Cursor for LabourReadModel {
    fn id(&self) -> Uuid {
        self.labour_id
    }

    fn updated_at(&self) -> DateTime<Utc> {
        self.updated_at
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct LabourRow {
    pub labour_id: String,
    pub birthing_person_id: String,
    pub current_phase: String,
    pub first_labour: String,
    pub due_date: String,
    pub labour_name: Option<String>,
    pub start_time: Option<String>,
    pub end_time: Option<String>,
    pub notes: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl LabourRow {
    pub fn into_read_model(self) -> Result<LabourReadModel> {
        Ok(LabourReadModel {
            labour_id: Uuid::parse_str(&self.labour_id)
                .map_err(|e| anyhow!("Invalid labour_id UUID: {}", e))?,
            birthing_person_id: self.birthing_person_id,
            current_phase: Self::parse_labour_phase(&self.current_phase)?,
            first_labour: Self::parse_bool(&self.first_labour)?,
            due_date: Self::parse_timestamp(&self.due_date)?,
            labour_name: self.labour_name,
            start_time: Self::parse_optional_timestamp(self.start_time)?,
            end_time: Self::parse_optional_timestamp(self.end_time)?,
            notes: self.notes,
            created_at: Self::parse_timestamp(&self.created_at)?,
            updated_at: Self::parse_timestamp(&self.updated_at)?,
        })
    }

    pub fn from_read_model(model: &LabourReadModel) -> Result<Self> {
        Ok(Self {
            labour_id: model.labour_id.to_string(),
            birthing_person_id: model.birthing_person_id.clone(),
            current_phase: model.current_phase.to_string(),
            first_labour: model.first_labour.to_string(),
            due_date: model.due_date.to_rfc3339(),
            labour_name: model.labour_name.clone(),
            start_time: model.start_time.map(|dt| dt.to_rfc3339()),
            end_time: model.end_time.map(|dt| dt.to_rfc3339()),
            notes: model.notes.clone(),
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

    fn parse_optional_timestamp(timestamp: Option<String>) -> Result<Option<DateTime<Utc>>> {
        match timestamp {
            Some(timestamp) => {
                let parsed_timestamp = Self::parse_timestamp(&timestamp)?;
                Ok(Some(parsed_timestamp))
            }
            _ => Ok(None),
        }
    }

    fn parse_bool(value: &str) -> Result<bool> {
        value
            .parse::<bool>()
            .map_err(|e| anyhow!("Invalid boolean value '{}': {}", value, e))
    }
}
