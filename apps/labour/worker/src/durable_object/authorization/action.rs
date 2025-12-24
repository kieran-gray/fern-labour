use uuid::Uuid;

use crate::durable_object::write_side::domain::{
    LabourCommand,
    commands::subscriber::{Unsubscribe, UpdateAccessLevel, UpdateNotificationMethods},
};

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
                LabourCommand::Unsubscribe(Unsubscribe {
                    subscription_id, ..
                })
                | LabourCommand::UpdateNotificationMethods(UpdateNotificationMethods {
                    subscription_id,
                    ..
                })
                | LabourCommand::UpdateAccessLevel(UpdateAccessLevel {
                    subscription_id, ..
                }),
            ) => Some(*subscription_id),

            _ => None,
        }
    }
}
