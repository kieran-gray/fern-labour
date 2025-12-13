use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum PublicCommand {
    #[serde(rename = "PlanLabour")]
    PlanLabour {
        first_labour: bool,
        due_date: DateTime<Utc>,
        labour_name: Option<String>,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum LabourCommand {
    #[serde(rename = "UpdateLabourPlan")]
    UpdateLabourPlan {
        labour_id: Uuid,
        first_labour: bool,
        due_date: DateTime<Utc>,
        labour_name: Option<String>,
    },

    #[serde(rename = "BeginLabour")]
    BeginLabour { labour_id: Uuid },

    #[serde(rename = "CompleteLabour")]
    CompleteLabour {
        labour_id: Uuid,
        notes: Option<String>,
    },

    #[serde(rename = "SendLabourInvite")]
    SendLabourInvite {
        labour_id: Uuid,
        invite_email: String,
    },

    #[serde(rename = "DeleteLabour")]
    DeleteLabour { labour_id: Uuid },
}

impl LabourCommand {
    pub fn labour_id(&self) -> Uuid {
        match self {
            LabourCommand::UpdateLabourPlan { labour_id, .. } => *labour_id,
            LabourCommand::BeginLabour { labour_id, .. } => *labour_id,
            LabourCommand::CompleteLabour { labour_id, .. } => *labour_id,
            LabourCommand::SendLabourInvite { labour_id, .. } => *labour_id,
            LabourCommand::DeleteLabour { labour_id, .. } => *labour_id,
        }
    }
}
