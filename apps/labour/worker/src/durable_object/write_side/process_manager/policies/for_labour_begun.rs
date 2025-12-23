use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};
use fern_labour_labour_shared::value_objects::subscriber::status::SubscriberStatus;

use crate::durable_object::write_side::{
    domain::{Labour, events::LabourBegun},
    process_manager::types::{
        Effect, IdempotencyKey, NotificationContext, NotificationIntent, SubscriberNotification,
    },
};

impl HasPolicies<Labour, Effect> for LabourBegun {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[notify_subscribers_on_start]
    }
}

fn notify_subscribers_on_start(event: &LabourBegun, ctx: &PolicyContext<Labour>) -> Vec<Effect> {
    let sender_id = ctx.state.mother_id().to_string();

    ctx.state
        .subscriptions()
        .iter()
        .filter(|s| s.status() == &SubscriberStatus::SUBSCRIBED)
        .flat_map(|subscription| {
            let sender_id = sender_id.clone();
            subscription.contact_methods().iter().map(move |channel| {
                Effect::SendNotification(NotificationIntent {
                    idempotency_key: IdempotencyKey::for_notification(
                        event.labour_id,
                        ctx.sequence,
                        subscription.subscriber_id(),
                        "labour_started",
                    ),
                    context: NotificationContext::Subscriber {
                        recipient_user_id: subscription.subscriber_id().to_string(),
                        subscription_id: subscription.id(),
                        channel: channel.clone(),
                        sender_id: sender_id.clone(),
                        notification: SubscriberNotification::LabourStarted {
                            labour_id: event.labour_id,
                        },
                    },
                })
            })
        })
        .collect()
}
