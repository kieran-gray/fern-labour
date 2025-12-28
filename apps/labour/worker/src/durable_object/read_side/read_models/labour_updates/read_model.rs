use std::str::FromStr;

use anyhow::{Result, anyhow};
use chrono::{DateTime, Utc};
use fern_labour_event_sourcing_rs::Cursor;
use fern_labour_labour_shared::value_objects::LabourUpdateType;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LabourUpdateReadModel {
    pub labour_id: Uuid,
    pub labour_update_id: Uuid,
    pub labour_update_type: LabourUpdateType,
    pub message: String,
    pub edited: bool,
    pub application_generated: bool,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl LabourUpdateReadModel {
    pub fn new(
        labour_id: Uuid,
        labour_update_id: Uuid,
        labour_update_type: LabourUpdateType,
        message: String,
        application_generated: bool,
        created_at: DateTime<Utc>,
    ) -> Self {
        Self {
            labour_id,
            labour_update_id,
            labour_update_type,
            message,
            edited: false,
            application_generated,
            created_at,
            updated_at: created_at,
        }
    }
}

impl Cursor for LabourUpdateReadModel {
    fn id(&self) -> Uuid {
        self.labour_update_id
    }

    fn updated_at(&self) -> DateTime<Utc> {
        self.created_at
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct LabourUpdateRow {
    pub labour_id: String,
    pub labour_update_id: String,
    pub labour_update_type: String,
    pub message: String,
    pub edited: String,
    pub application_generated: String,
    pub created_at: String,
    pub updated_at: String,
}

impl LabourUpdateRow {
    pub fn into_read_model(self) -> Result<LabourUpdateReadModel> {
        Ok(LabourUpdateReadModel {
            labour_id: Uuid::parse_str(&self.labour_id)
                .map_err(|e| anyhow!("Invalid labour_id UUID: {}", e))?,
            labour_update_id: Uuid::parse_str(&self.labour_update_id)
                .map_err(|e| anyhow!("Invalid labour_update_id UUID: {}", e))?,
            labour_update_type: LabourUpdateType::from_str(&self.labour_update_type)
                .map_err(|e| anyhow!("Invalid labour_update_type: {}", e))?,
            message: self.message,
            edited: Self::parse_bool(&self.edited)?,
            application_generated: Self::parse_bool(&self.application_generated)?,
            created_at: Self::parse_timestamp(&self.created_at)?,
            updated_at: Self::parse_timestamp(&self.updated_at)?,
        })
    }

    pub fn from_read_model(model: &LabourUpdateReadModel) -> Result<Self> {
        Ok(Self {
            labour_id: model.labour_id.to_string(),
            labour_update_id: model.labour_update_id.to_string(),
            labour_update_type: model.labour_update_type.to_string(),
            message: model.message.clone(),
            edited: Self::bool_to_string(model.edited),
            application_generated: Self::bool_to_string(model.application_generated),
            created_at: model.created_at.to_rfc3339(),
            updated_at: model.updated_at.to_rfc3339(),
        })
    }

    fn parse_timestamp(timestamp: &str) -> Result<DateTime<Utc>> {
        let datetime = DateTime::parse_from_rfc3339(timestamp)
            .map_err(|e| anyhow!("Invalid timestamp: {}", e))?
            .with_timezone(&Utc);
        Ok(datetime)
    }

    fn parse_bool(value: &str) -> Result<bool> {
        match value {
            "true" | "1" => Ok(true),
            "false" | "0" => Ok(false),
            _ => Err(anyhow!("Invalid boolean value: {}", value)),
        }
    }

    fn bool_to_string(value: bool) -> String {
        if value { "true" } else { "false" }.to_string()
    }
}
