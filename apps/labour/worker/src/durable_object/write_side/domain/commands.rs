use chrono::{DateTime, Utc};
use fern_labour_labour_shared::{
    ContractionCommand, LabourUpdateCommand, SubscriberCommand, SubscriptionCommand,
    commands::labour::LabourCommand as LabourApiCommand,
    value_objects::{
        LabourUpdateType, SubscriberAccessLevel, SubscriberContactMethod, SubscriberRole,
    },
};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Deserialize, Serialize)]
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
    // Subscriber Commands
    RequestAccess {
        labour_id: Uuid,
        subscriber_id: String,
        token: String,
    },
    Unsubscribe {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    UpdateNotificationMethods {
        labour_id: Uuid,
        subscription_id: Uuid,
        notification_methods: Vec<SubscriberContactMethod>,
    },
    UpdateAccessLevel {
        labour_id: Uuid,
        subscription_id: Uuid,
        access_level: SubscriberAccessLevel,
    },
    // Subscription Commands
    SetSubscriptionToken {
        labour_id: Uuid,
        mother_id: String,
        token: String,
    },
    ApproveSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    RemoveSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    BlockSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    UnblockSubscriber {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    UpdateSubscriberRole {
        labour_id: Uuid,
        subscription_id: Uuid,
        role: SubscriberRole,
    },
}

impl From<LabourApiCommand> for LabourCommand {
    fn from(cmd: LabourApiCommand) -> Self {
        match cmd {
            LabourApiCommand::PlanLabour {
                labour_id,
                mother_id,
                mother_name,
                first_labour,
                due_date,
                labour_name,
            } => LabourCommand::PlanLabour {
                labour_id,
                mother_id,
                mother_name,
                first_labour,
                due_date,
                labour_name,
            },
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

impl From<(SubscriberCommand, String)> for LabourCommand {
    fn from((cmd, subscriber_id): (SubscriberCommand, String)) -> Self {
        match cmd {
            SubscriberCommand::RequestAccess { labour_id, token } => LabourCommand::RequestAccess {
                labour_id,
                subscriber_id,
                token,
            },
            SubscriberCommand::Unsubscribe {
                labour_id,
                subscription_id,
            } => LabourCommand::Unsubscribe {
                labour_id,
                subscription_id,
            },
            SubscriberCommand::UpdateAccessLevel {
                labour_id,
                access_level,
                subscription_id,
            } => LabourCommand::UpdateAccessLevel {
                labour_id,
                subscription_id,
                access_level,
            },
            SubscriberCommand::UpdateNotificationMethods {
                labour_id,
                subscription_id,
                notification_methods,
            } => LabourCommand::UpdateNotificationMethods {
                labour_id,
                subscription_id,
                notification_methods,
            },
        }
    }
}

impl From<SubscriptionCommand> for LabourCommand {
    fn from(cmd: SubscriptionCommand) -> Self {
        match cmd {
            SubscriptionCommand::ApproveSubscriber {
                labour_id,
                subscription_id,
            } => LabourCommand::ApproveSubscriber {
                labour_id,
                subscription_id,
            },
            SubscriptionCommand::BlockSubscriber {
                labour_id,
                subscription_id,
            } => LabourCommand::BlockSubscriber {
                labour_id,
                subscription_id,
            },
            SubscriptionCommand::RemoveSubscriber {
                labour_id,
                subscription_id,
            } => LabourCommand::RemoveSubscriber {
                labour_id,
                subscription_id,
            },
            SubscriptionCommand::UnblockSubscriber {
                labour_id,
                subscription_id,
            } => LabourCommand::UnblockSubscriber {
                labour_id,
                subscription_id,
            },
            SubscriptionCommand::UpdateSubscriberRole {
                labour_id,
                subscription_id,
                role,
            } => LabourCommand::UpdateSubscriberRole {
                labour_id,
                subscription_id,
                role,
            },
        }
    }
}
