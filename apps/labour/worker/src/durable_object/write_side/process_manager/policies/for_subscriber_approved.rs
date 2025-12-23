use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};
use fern_labour_labour_shared::value_objects::SubscriberContactMethod;

use crate::durable_object::write_side::{
    domain::{Labour, events::SubscriberApproved},
    process_manager::types::{
        Effect, IdempotencyKey, NotificationContext, NotificationIntent, SubscriberNotification,
    },
};

impl HasPolicies<Labour, Effect> for SubscriberApproved {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[notify_subscriber_on_approval]
    }
}

fn notify_subscriber_on_approval(
    event: &SubscriberApproved,
    ctx: &PolicyContext<Labour>,
) -> Vec<Effect> {
    let sender_id = ctx.state.mother_id().to_string();

    let subscription = ctx
        .state
        .subscriptions()
        .iter()
        .find(|s| s.id() == event.subscription_id);

    match subscription {
        Some(subscription) => {
            vec![Effect::SendNotification(NotificationIntent {
                idempotency_key: IdempotencyKey::for_notification(
                    event.labour_id,
                    ctx.sequence,
                    subscription.subscriber_id(),
                    "approved",
                ),
                context: NotificationContext::Subscriber {
                    recipient_user_id: subscription.subscriber_id().to_string(),
                    subscription_id: subscription.id(),
                    channel: SubscriberContactMethod::EMAIL,
                    sender_id: sender_id.clone(),
                    notification: SubscriberNotification::SubscriptionApproved {
                        labour_id: event.labour_id,
                    },
                },
            })]
        }
        None => vec![],
    }
}
