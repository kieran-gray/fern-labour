use chrono::{DateTime, Utc};
use fern_labour_labour_shared::value_objects::LabourUpdateType;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LabourUpdate {
    id: Uuid,
    labour_id: Uuid,
    labour_update_type: LabourUpdateType,
    message: String,
    sent_time: DateTime<Utc>,
    edited: bool,
    application_generated: bool,
}

impl LabourUpdate {
    pub fn create(
        labour_id: Uuid,
        labour_update_id: Uuid,
        labour_update_type: LabourUpdateType,
        message: String,
        sent_time: DateTime<Utc>,
        application_generated: bool,
    ) -> Self {
        Self {
            id: labour_update_id,
            labour_id,
            labour_update_type,
            message,
            sent_time,
            edited: false,
            application_generated,
        }
    }

    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn labour_update_type(&self) -> &LabourUpdateType {
        &self.labour_update_type
    }

    pub fn sent_time(&self) -> &DateTime<Utc> {
        &self.sent_time
    }
}
