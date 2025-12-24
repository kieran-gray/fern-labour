use std::collections::HashSet;

use fern_labour_labour_shared::value_objects::{
    SubscriberRole, subscriber::status::SubscriberStatus,
};

use crate::durable_object::{
    authorization::{Action, Principal, QueryAction},
    write_side::domain::LabourCommand,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Capability {
    PostApplicationLabourUpdates,
    ManageLabour,
    ExecuteLabourCommand,
    ReadLabour,
    UpdateSubscriptionAccessLevel,
    ManageOwnSubscription,
    ManageLabourSubscriptions,
    ManageSubscriptionToken,
    ReadSubscriptions,
    ReadOwnSubscription,
}

pub fn capabilities_for(principal: &Principal) -> HashSet<Capability> {
    match principal {
        Principal::Mother => HashSet::from([
            Capability::ManageLabour,
            Capability::ExecuteLabourCommand,
            Capability::ReadLabour,
            Capability::ManageLabourSubscriptions,
            Capability::ReadSubscriptions,
        ]),

        Principal::Subscriber { role, status, .. } => {
            if *status != SubscriberStatus::SUBSCRIBED {
                return HashSet::new();
            }

            match role {
                SubscriberRole::BIRTH_PARTNER => HashSet::from([
                    Capability::ExecuteLabourCommand,
                    Capability::ReadLabour,
                    Capability::ManageOwnSubscription,
                ]),
                SubscriberRole::FRIENDS_AND_FAMILY => {
                    HashSet::from([Capability::ReadLabour, Capability::ManageOwnSubscription])
                }
            }
        }

        Principal::Internal => HashSet::from([
            Capability::PostApplicationLabourUpdates,
            Capability::ManageSubscriptionToken,
            Capability::UpdateSubscriptionAccessLevel,
        ]),

        Principal::Unassociated => HashSet::new(),
    }
}

pub fn required_capability(action: &Action) -> Capability {
    match action {
        Action::Command(cmd) => match cmd {
            LabourCommand::PlanLabour(..)
            | LabourCommand::DeleteLabour(..)
            | LabourCommand::SendLabourInvite(..) => Capability::ManageLabour,

            LabourCommand::UpdateLabourPlan(..)
            | LabourCommand::BeginLabour(..)
            | LabourCommand::CompleteLabour(..)
            | LabourCommand::StartContraction(..)
            | LabourCommand::EndContraction(..)
            | LabourCommand::UpdateContraction(..)
            | LabourCommand::DeleteContraction(..)
            | LabourCommand::PostLabourUpdate(..)
            | LabourCommand::UpdateLabourUpdateMessage(..)
            | LabourCommand::UpdateLabourUpdateType(..)
            | LabourCommand::DeleteLabourUpdate(..) => Capability::ExecuteLabourCommand,

            LabourCommand::PostApplicationLabourUpdate(..) => {
                Capability::PostApplicationLabourUpdates
            }

            LabourCommand::RequestAccess(..)
            | LabourCommand::Unsubscribe(..)
            | LabourCommand::UpdateNotificationMethods(..) => Capability::ManageOwnSubscription,

            LabourCommand::UpdateAccessLevel(..) => Capability::UpdateSubscriptionAccessLevel,

            LabourCommand::SetSubscriptionToken(..) => Capability::ManageSubscriptionToken,

            LabourCommand::ApproveSubscriber(..)
            | LabourCommand::RemoveSubscriber(..)
            | LabourCommand::BlockSubscriber(..)
            | LabourCommand::UnblockSubscriber(..)
            | LabourCommand::UpdateSubscriberRole(..) => Capability::ManageLabourSubscriptions,
        },

        Action::Query(q) => match q {
            QueryAction::GetLabour
            | QueryAction::GetContractions
            | QueryAction::GetLabourUpdates => Capability::ReadLabour,

            QueryAction::GetUserSubscription => Capability::ReadOwnSubscription,

            QueryAction::GetSubscriptionToken
            | QueryAction::GetLabourSubscriptions
            | QueryAction::GetUser
            | QueryAction::GetUsers => Capability::ReadSubscriptions,
        },
    }
}
