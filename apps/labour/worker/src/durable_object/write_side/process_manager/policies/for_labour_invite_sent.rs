use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};

use crate::durable_object::write_side::{
    domain::{Labour, events::LabourInviteSent},
    process_manager::types::{
        Effect, EmailNotification, IdempotencyKey, NotificationContext, NotificationIntent,
    },
};

impl HasPolicies<Labour, Effect> for LabourInviteSent {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[send_labour_invite_email]
    }
}

fn send_labour_invite_email(event: &LabourInviteSent, ctx: &PolicyContext<Labour>) -> Vec<Effect> {
    let sender_id = ctx.state.mother_id().to_string();

    vec![Effect::SendNotification(NotificationIntent {
        idempotency_key: IdempotencyKey::for_notification(
            event.labour_id,
            ctx.sequence,
            &event.invite_email,
            "invite",
        ),
        context: NotificationContext::Email {
            email: event.invite_email.clone(),
            sender_id,
            notification: EmailNotification::LabourInvite {
                labour_id: event.labour_id,
            },
        },
    })]
}
