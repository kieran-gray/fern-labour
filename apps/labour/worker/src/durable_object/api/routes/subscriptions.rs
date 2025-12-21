use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_labour_shared::{
    ApiQuery, SubscriberCommand, SubscriptionCommand, queries::subscription::SubscriptionQuery,
};
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    api::{ApiResult, router::RequestContext},
    read_side::query_handler::QueryHandler,
    write_side::domain::LabourCommand,
};

pub async fn handle_subscriber_command(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(envelope) = req.json::<CommandEnvelope<SubscriberCommand>>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(
        aggregate_id = %envelope.metadata.aggregate_id,
        correlation_id = %envelope.metadata.correlation_id,
        user_id = %envelope.metadata.user_id,
        auth_user_id = %user.user_id,
        idempotency_key = %envelope.metadata.idempotency_key,
        "Processing subscriber command"
    );

    let domain_command = LabourCommand::from((envelope.command.clone(), user.user_id.clone()));

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

pub async fn handle_subscription_command(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(envelope) = req.json::<CommandEnvelope<SubscriptionCommand>>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(
        aggregate_id = %envelope.metadata.aggregate_id,
        correlation_id = %envelope.metadata.correlation_id,
        user_id = %envelope.metadata.user_id,
        auth_user_id = %user.user_id,
        idempotency_key = %envelope.metadata.idempotency_key,
        "Processing subscription command"
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

pub async fn handle_subscription_query(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(query) = req.json::<SubscriptionQuery>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(query = ?query, auth_user_id = %user.user_id, "Processing subscription query");

    let handler = QueryHandler::new(ctx.data.read_model());
    let result = handler.handle(ApiQuery::Subscription(query), &user);

    if let Err(ref err) = result {
        error!("Query execution failed: {}", err);
    } else {
        info!("Query executed successfully");
    }

    Ok(ApiResult::from_json_result(result).into_response())
}
