use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_labour_shared::{LabourCommand as LabourAPICommand, LabourQuery};
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    api::ApiResult, api::router::RequestContext,
    read_side::read_models::labour::LabourReadModelQueryHandler, write_side::domain::LabourCommand,
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
        error!("Command execution failed: {}", err);
    } else {
        info!("Command executed successfully");
    }

    Ok(ApiResult::from_unit_result(result).into_response())
}

pub async fn handle_labour_api_command(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(envelope) = req.json::<CommandEnvelope<LabourAPICommand>>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(
        aggregate_id = %envelope.metadata.aggregate_id,
        correlation_id = %envelope.metadata.correlation_id,
        user_id = %envelope.metadata.user_id,
        auth_user_id = %user.user_id,
        idempotency_key = %envelope.metadata.idempotency_key,
        "Processing labour command"
    );

    let domain_command = LabourCommand::from(envelope.command);

    let result = ctx
        .data
        .write_model()
        .labour_command_processor
        .handle_command(domain_command, user);

    if let Err(ref err) = result {
        error!("Command execution failed: {}", err);
    } else {
        info!("Command executed successfully");
    }

    Ok(ApiResult::from_unit_result(result).into_response())
}

pub async fn handle_labour_query(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(query) = req.json::<LabourQuery>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(query = ?query, auth_user_id = %user.user_id, "Processing labour query");

    let result = match query {
        LabourQuery::GetLabour { labour_id } => {
            info!(labour_id = %labour_id, "Getting labour");
            ctx.data.read_model().labour_query.get()
        }
    };

    if let Err(ref err) = result {
        error!("Query execution failed: {}", err);
    } else {
        info!("Query executed successfully");
    }

    Ok(ApiResult::from_json_result(result).into_response())
}
