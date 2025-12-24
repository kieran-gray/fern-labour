use uuid::Uuid;

use crate::durable_object::write_side::domain::LabourCommand;

#[derive(Debug, Clone)]
pub enum Action {
    Command(LabourCommand),
    Query(QueryAction),
}

#[derive(Debug, Clone)]
pub enum QueryAction {
    GetLabour,
    GetContractions,
    GetLabourUpdates,
    GetSubscriptionToken,
    GetLabourSubscriptions,
    GetUserSubscription,
    GetUser,
    GetUsers,
}

impl Action {
    pub fn subscription_target(&self) -> Option<Uuid> {
        match self {
            Action::Command(
                LabourCommand::Unsubscribe {
                    subscription_id, ..
                }
                | LabourCommand::UpdateNotificationMethods {
                    subscription_id, ..
                }
                | LabourCommand::UpdateAccessLevel {
                    subscription_id, ..
                },
            ) => Some(*subscription_id),

            _ => None,
        }
    }
}
