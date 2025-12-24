use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};
use fern_labour_labour_shared::value_objects::{
    LabourUpdateType, subscriber::status::SubscriberStatus,
};

use crate::durable_object::write_side::{
    domain::{Labour, events::LabourUpdateTypeUpdated},
    process_manager::types::{
        Effect, IdempotencyKey, NotificationContext, NotificationIntent, SubscriberNotification,
    },
};

impl HasPolicies<Labour, Effect> for LabourUpdateTypeUpdated {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[notifiy_subscribers_on_status_update_announcement]
    }
}

fn notifiy_subscribers_on_status_update_announcement(
    event: &LabourUpdateTypeUpdated,
    ctx: &PolicyContext<Labour>,
) -> Vec<Effect> {
    if event.labour_update_type != LabourUpdateType::ANNOUNCEMENT {
        return vec![];
    };
    let Some(labour_update) = ctx.state.find_labour_update(event.labour_update_id) else {
        return vec![];
    };

    let notification_type = match labour_update.application_generated() {
        true => labour_update.message(),
        _ => "announcement",
    };

    let notification_content = match notification_type {
        "labour_begun" => SubscriberNotification::LabourBegun {
            labour_id: event.labour_id,
        },
        "announcement" => SubscriberNotification::AnnouncementPosted {
            labour_id: event.labour_id,
            message: labour_update.message().to_string(),
        },
        _ => return vec![],
    };

    let sender_id = ctx.state.mother_id().to_string();

    ctx.state
        .subscriptions()
        .iter()
        .filter(|s| s.status() == &SubscriberStatus::SUBSCRIBED)
        .flat_map(|subscription| {
            let sender_id = sender_id.clone();
            let content = notification_content.clone();
            subscription.contact_methods().iter().map(move |channel| {
                Effect::SendNotification(NotificationIntent {
                    idempotency_key: IdempotencyKey::for_notification(
                        event.labour_id,
                        ctx.sequence,
                        subscription.subscriber_id(),
                        notification_type,
                    ),
                    context: NotificationContext::Subscriber {
                        recipient_user_id: subscription.subscriber_id().to_string(),
                        subscription_id: subscription.id(),
                        channel: channel.clone(),
                        sender_id: sender_id.clone(),
                        notification: content.clone(),
                    },
                })
            })
        })
        .collect()
}
