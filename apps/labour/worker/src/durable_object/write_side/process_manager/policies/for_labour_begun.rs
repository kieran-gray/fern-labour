use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};
use fern_labour_labour_shared::value_objects::subscriber::status::SubscriberStatus;

use crate::durable_object::write_side::{
    domain::{
        Labour, LabourCommand, commands::labour_update::PostApplicationLabourUpdate,
        events::LabourBegun,
    },
    process_manager::types::{
        Effect, IdempotencyKey, NotificationContext, NotificationIntent, SubscriberNotification,
    },
};

impl HasPolicies<Labour, Effect> for LabourBegun {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[
            notify_subscribers_on_start,
            post_application_generated_labour_begun_message,
        ]
    }
}

fn notify_subscribers_on_start(event: &LabourBegun, ctx: &PolicyContext<Labour>) -> Vec<Effect> {
    let sender_id = ctx.state.mother_id().to_string();
    // TODO: this should not cause a notification
    // The flow should be:
    // - LabourBegun
    // - Add application generated labour update
    // - LabourUpdateTypeUpdated
    // - Then share the labour begun message

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
                        "labour_begun",
                    ),
                    context: NotificationContext::Subscriber {
                        recipient_user_id: subscription.subscriber_id().to_string(),
                        subscription_id: subscription.id(),
                        channel: channel.clone(),
                        sender_id: sender_id.clone(),
                        notification: SubscriberNotification::LabourBegun {
                            labour_id: event.labour_id,
                        },
                    },
                })
            })
        })
        .collect()
}

fn post_application_generated_labour_begun_message(
    event: &LabourBegun,
    ctx: &PolicyContext<Labour>,
) -> Vec<Effect> {
    vec![Effect::IssueCommand {
        idempotency_key: IdempotencyKey::for_command(
            event.labour_id,
            ctx.sequence,
            "application_labour_update",
        ),
        command: LabourCommand::PostApplicationLabourUpdate(PostApplicationLabourUpdate {
            labour_id: event.labour_id,
            message: "labour_begun".to_string(),
        }),
    }]
}
