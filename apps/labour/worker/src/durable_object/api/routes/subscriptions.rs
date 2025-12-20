use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_labour_shared::{
    SubscriberCommand, SubscriptionCommand, queries::subscription::SubscriptionQuery,
};
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    api::{ApiResult, router::RequestContext, utils::build_paginated_response},
    read_side::read_models::{
        subscription_token::SubscriptionTokenQueryHandler, subscriptions::SubscriptionQueryHandler,
    },
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

    let result = match query {
        SubscriptionQuery::GetSubscriptionToken { labour_id } => {
            info!(labour_id = %labour_id, user_id = %user.user_id, "Getting subscription token");
            let token = match ctx.data.read_model().subscription_token_query.get() {
                Ok(Some(token)) => token.token,
                Ok(_) | Err(_) => return Response::error("No subcription token available", 400),
            };
            ApiResult::from_json_result(Ok(serde_json::json!({ "token": token })))
        }
        SubscriptionQuery::GetLabourSubscriptions { labour_id } => {
            info!(labour_id = %labour_id, user_id = %user.user_id, "Getting subscriptions");
            let subscriptions = ctx
                .data
                .read_model()
                .subscription_query
                .get(100, None) // TODO
                .map(|items| build_paginated_response(items, 100));
            ApiResult::from_json_result(subscriptions)
        }
        SubscriptionQuery::GetUserSubscription { labour_id } => {
            info!(labour_id = %labour_id, user_id = %user.user_id, "Getting subscriptions");
            let subscription = ctx
                .data
                .read_model()
                .subscription_query
                .get_user_subscription(user.user_id);
            ApiResult::from_json_result(subscription)
        }
    };

    Ok(result.into_response())
}
