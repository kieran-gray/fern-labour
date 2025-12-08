use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::durable_object::write_side::domain::LabourCommand;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlanLabourDTO {
    pub first_labour: bool,
    pub due_date: DateTime<Utc>,
    pub labour_name: Option<String>,
}

impl PlanLabourDTO {
    pub fn into_domain(self, labour_id: Uuid, user_id: String) -> LabourCommand {
        LabourCommand::PlanLabour {
            labour_id,
            birthing_person_id: user_id,
            first_labour: self.first_labour,
            due_date: self.due_date,
            labour_name: self.labour_name,
        }
    }
}
