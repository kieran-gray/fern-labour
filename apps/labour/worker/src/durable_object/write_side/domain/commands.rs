use anyhow::Result;
use chrono::{DateTime, Utc};
use fern_labour_labour_shared::{
    ContractionCommand, LabourUpdateCommand,
    commands::labour::{LabourCommand as LabourApiCommand, PublicCommand},
    value_objects::LabourUpdateType,
};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum LabourCommand {
    PlanLabour {
        labour_id: Uuid,
        birthing_person_id: String,
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
    // Contraction Commands
    StartContraction {
        labour_id: Uuid,
        start_time: DateTime<Utc>,
    },
    EndContraction {
        labour_id: Uuid,
        end_time: DateTime<Utc>,
        intensity: u8,
    },
    UpdateContraction {
        labour_id: Uuid,
        contraction_id: Uuid,
        start_time: Option<DateTime<Utc>>,
        end_time: Option<DateTime<Utc>>,
        intensity: Option<u8>,
    },
    DeleteContraction {
        labour_id: Uuid,
        contraction_id: Uuid,
    },
    // Labour Update Commands
    PostLabourUpdate {
        labour_id: Uuid,
        labour_update_type: LabourUpdateType,
        message: String,
    },
    UpdateLabourUpdateMessage {
        labour_id: Uuid,
        labour_update_id: Uuid,
        message: String,
    },
    UpdateLabourUpdateType {
        labour_id: Uuid,
        labour_update_id: Uuid,
        labour_update_type: LabourUpdateType,
    },
    DeleteLabourUpdate {
        labour_id: Uuid,
        labour_update_id: Uuid,
    },
}

impl TryFrom<(PublicCommand, Uuid, String)> for LabourCommand {
    type Error = anyhow::Error;
    fn try_from(
        (command, labour_id, birthing_person_id): (PublicCommand, Uuid, String),
    ) -> Result<Self> {
        match command {
            PublicCommand::PlanLabour {
                first_labour,
                due_date,
                labour_name,
            } => Ok(LabourCommand::PlanLabour {
                labour_id,
                birthing_person_id,
                first_labour,
                due_date,
                labour_name,
            }),
        }
    }
}

impl From<LabourApiCommand> for LabourCommand {
    fn from(cmd: LabourApiCommand) -> Self {
        match cmd {
            LabourApiCommand::UpdateLabourPlan {
                labour_id,
                first_labour,
                due_date,
                labour_name,
            } => LabourCommand::UpdateLabourPlan {
                labour_id,
                first_labour,
                due_date,
                labour_name,
            },
            LabourApiCommand::BeginLabour { labour_id } => LabourCommand::BeginLabour { labour_id },
            LabourApiCommand::CompleteLabour { labour_id, notes } => {
                LabourCommand::CompleteLabour { labour_id, notes }
            }
            LabourApiCommand::SendLabourInvite {
                labour_id,
                invite_email,
            } => LabourCommand::SendLabourInvite {
                labour_id,
                invite_email,
            },
            LabourApiCommand::DeleteLabour { labour_id } => {
                LabourCommand::DeleteLabour { labour_id }
            }
        }
    }
}

impl From<ContractionCommand> for LabourCommand {
    fn from(cmd: ContractionCommand) -> Self {
        match cmd {
            ContractionCommand::StartContraction {
                labour_id,
                start_time,
            } => LabourCommand::StartContraction {
                labour_id,
                start_time,
            },
            ContractionCommand::EndContraction {
                labour_id,
                end_time,
                intensity,
            } => LabourCommand::EndContraction {
                labour_id,
                end_time,
                intensity,
            },
            ContractionCommand::UpdateContraction {
                labour_id,
                contraction_id,
                start_time,
                end_time,
                intensity,
            } => LabourCommand::UpdateContraction {
                labour_id,
                contraction_id,
                start_time,
                end_time,
                intensity,
            },
            ContractionCommand::DeleteContraction {
                labour_id,
                contraction_id,
            } => LabourCommand::DeleteContraction {
                labour_id,
                contraction_id,
            },
        }
    }
}

impl From<LabourUpdateCommand> for LabourCommand {
    fn from(cmd: LabourUpdateCommand) -> Self {
        match cmd {
            LabourUpdateCommand::PostLabourUpdate {
                labour_id,
                labour_update_type,
                message,
            } => LabourCommand::PostLabourUpdate {
                labour_id,
                labour_update_type,
                message,
            },
            LabourUpdateCommand::UpdateLabourUpdateMessage {
                labour_id,
                labour_update_id,
                message,
            } => LabourCommand::UpdateLabourUpdateMessage {
                labour_id,
                labour_update_id,
                message,
            },
            LabourUpdateCommand::UpdateLabourUpdateType {
                labour_id,
                labour_update_id,
                labour_update_type,
            } => LabourCommand::UpdateLabourUpdateType {
                labour_id,
                labour_update_id,
                labour_update_type,
            },
            LabourUpdateCommand::DeleteLabourUpdate {
                labour_id,
                labour_update_id,
            } => LabourCommand::DeleteLabourUpdate {
                labour_id,
                labour_update_id,
            },
        }
    }
}
