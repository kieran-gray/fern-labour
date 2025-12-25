use fern_labour_event_sourcing_rs::{HasPolicies, PolicyContext, PolicyFn};

use crate::durable_object::write_side::{
    domain::{
        Labour, LabourCommand, commands::labour_update::PostApplicationLabourUpdate,
        events::LabourBegun,
    },
    process_manager::types::{Effect, IdempotencyKey},
};

impl HasPolicies<Labour, Effect> for LabourBegun {
    fn policies() -> &'static [PolicyFn<Self, Labour, Effect>] {
        &[post_application_generated_labour_begun_message]
    }
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
