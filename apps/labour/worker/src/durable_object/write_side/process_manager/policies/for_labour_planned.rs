use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};

use crate::durable_object::write_side::{
    domain::{Labour, events::LabourPlanned},
    process_manager::types::{Effect, IdempotencyKey},
};

impl HasPolicies<Labour, Effect> for LabourPlanned {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[generate_subscription_token]
    }
}

fn generate_subscription_token(event: &LabourPlanned, ctx: &PolicyContext<Labour>) -> Vec<Effect> {
    vec![Effect::GenerateSubscriptionToken {
        labour_id: event.labour_id,
        mother_id: ctx.state.mother_id().to_string(),
        idempotency_key: IdempotencyKey::for_command(
            event.labour_id,
            ctx.sequence,
            "generate_subscription_token",
        ),
    }]
}
