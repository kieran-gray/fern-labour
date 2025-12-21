use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    http::{router::RequestContext, ApiResult},
    write_side::domain::LabourCommand,
};

pub async fn handle_labour_domain_command(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(envelope) = req.json::<CommandEnvelope<LabourCommand>>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(
        aggregate_id = %envelope.metadata.aggregate_id,
        correlation_id = %envelope.metadata.correlation_id,
        user_id = %envelope.metadata.user_id,
        auth_user_id = %user.user_id,
        idempotency_key = %envelope.metadata.idempotency_key,
        "Processing domain command"
    );

    let result = ctx
        .data
        .write_model()
        .labour_command_processor
        .handle_command(envelope.command, user);

    if let Err(ref err) = result {
        error!(error = %err, "Domain command execution failed");
    } else {
        info!("Domain command executed successfully");
    }

    Ok(ApiResult::from_unit_result(result).into_response())
}
