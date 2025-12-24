use chrono::{DateTime, Utc};
use fern_labour_workers_shared::User;
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
    pub fn into_domain(self, labour_id: Uuid, user: &User) -> LabourCommand {
        use crate::durable_object::write_side::domain::commands::labour::PlanLabour;

        LabourCommand::PlanLabour(PlanLabour {
            labour_id,
            mother_id: user.user_id.clone(),
            mother_name: user.name.clone().unwrap_or_default(),
            first_labour: self.first_labour,
            due_date: self.due_date,
            labour_name: self.labour_name,
        })
    }
}
