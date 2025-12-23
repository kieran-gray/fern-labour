use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum LabourCommand {
    PlanLabour {
        labour_id: Uuid,
        mother_id: String,
        mother_name: String,
        first_labour: bool,
        due_date: DateTime<Utc>,
        labour_name: Option<String>,
    },

    UpdateLabourPlan {
        labour_id: Uuid,
        first_labour: bool,
        due_date: DateTime<Utc>,
        labour_name: Option<String>,
    },

    BeginLabour {
        labour_id: Uuid,
    },

    CompleteLabour {
        labour_id: Uuid,
        notes: Option<String>,
    },

    SendLabourInvite {
        labour_id: Uuid,
        invite_email: String,
    },

    DeleteLabour {
        labour_id: Uuid,
    },
}

impl LabourCommand {
    pub fn labour_id(&self) -> Uuid {
        match self {
            LabourCommand::PlanLabour { labour_id, .. } => *labour_id,
            LabourCommand::UpdateLabourPlan { labour_id, .. } => *labour_id,
            LabourCommand::BeginLabour { labour_id, .. } => *labour_id,
            LabourCommand::CompleteLabour { labour_id, .. } => *labour_id,
            LabourCommand::SendLabourInvite { labour_id, .. } => *labour_id,
            LabourCommand::DeleteLabour { labour_id, .. } => *labour_id,
        }
    }
}
