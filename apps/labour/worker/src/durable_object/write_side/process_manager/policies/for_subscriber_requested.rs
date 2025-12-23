use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};
use fern_labour_labour_shared::value_objects::SubscriberContactMethod;

use crate::durable_object::write_side::{
    domain::{Labour, events::SubscriberRequested},
    process_manager::types::{
        Effect, IdempotencyKey, LabourOwnerNotification, NotificationContext, NotificationIntent,
    },
};

impl HasPolicies<Labour, Effect> for SubscriberRequested {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[notify_mother_on_subscriber_request]
    }
}

fn notify_mother_on_subscriber_request(
    event: &SubscriberRequested,
    ctx: &PolicyContext<Labour>,
) -> Vec<Effect> {
    let mother_id = ctx.state.mother_id().to_string();

    vec![Effect::SendNotification(NotificationIntent {
        idempotency_key: IdempotencyKey::for_notification(
            event.labour_id,
            ctx.sequence,
            &mother_id,
            "subscriber_requested",
        ),
        context: NotificationContext::LabourOwner {
            recipient_user_id: mother_id,
            channel: SubscriberContactMethod::EMAIL,
            notification: LabourOwnerNotification::SubscriberRequested {
                labour_id: event.labour_id,
                subscription_id: event.subscription_id,
                requester_user_id: event.subscriber_id.clone(),
            },
        },
    })]
}
