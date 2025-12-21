use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_labour_shared::{ApiQuery, ContractionCommand, ContractionQuery};
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    api::router::RequestContext,
    api::ApiResult,
    read_side::query_handler::QueryHandler,
    write_side::domain::LabourCommand,
};

pub async fn handle_contraction_command(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(envelope) = req.json::<CommandEnvelope<ContractionCommand>>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(
        aggregate_id = %envelope.metadata.aggregate_id,
        correlation_id = %envelope.metadata.correlation_id,
        user_id = %envelope.metadata.user_id,
        auth_user_id = %user.user_id,
        idempotency_key = %envelope.metadata.idempotency_key,
        "Processing contraction command"
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

pub async fn handle_contraction_query(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(query) = req.json::<ContractionQuery>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(query = ?query, auth_user_id = %user.user_id, "Processing contraction query");

    let handler = QueryHandler::new(ctx.data.read_model());
    let result = handler.handle(ApiQuery::Contraction(query), &user);

    if let Err(ref err) = result {
        error!("Query execution failed: {}", err);
    } else {
        info!("Query executed successfully");
    }

    Ok(ApiResult::from_json_result(result).into_response())
}
