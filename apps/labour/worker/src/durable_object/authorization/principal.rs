use fern_labour_labour_shared::value_objects::{
    SubscriberRole, subscriber::status::SubscriberStatus,
};
use fern_labour_workers_shared::User;

use crate::durable_object::write_side::domain::Labour;

#[derive(Debug, Clone, PartialEq)]
pub enum Principal {
    Mother,
    Subscriber {
        user_id: String,
        role: SubscriberRole,
        status: SubscriberStatus,
    },
    Internal,
    Unassociated,
}

pub fn resolve_principal(user: &User, aggregate: Option<&Labour>) -> Principal {
    let Some(aggregate) = aggregate else {
        return Principal::Unassociated;
    };

    if user.user_id == aggregate.mother_id() {
        return Principal::Mother;
    }

    if user.user_id.starts_with("fern-labour-internal") {
        return Principal::Internal;
    }

    for subscription in aggregate.subscriptions() {
        if subscription.subscriber_id() == user.user_id {
            return Principal::Subscriber {
                user_id: user.user_id.clone(),
                role: subscription.role().clone(),
                status: subscription.status().clone(),
            };
        }
    }

    Principal::Unassociated
}
