use fern_labour_workers_shared::{CorsContext, clients::worker_clients::auth::User};
use worker::{Request, Response, RouteContext};

use crate::{
    api_worker::AppState,
    durable_object::read_side::read_models::{labour_status::LabourStatusReadModelQueryHandler, subscription_status::SubscriptionStatusReadModelQueryHandler},
};

pub async fn get_user_subscriptions(
    _req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user: User,
) -> worker::Result<Response> {
    let subscription_status = ctx
        .data
        .subscription_status_query
        .get_by_user_id(user.user_id)
        .await
        .map_err(|e| format!("Failed to query subscription status: {e}"))?;

    let response = Response::from_json(&subscription_status)
        .map_err(|e| format!("Failed to serialize response: {e}"))?;

    Ok(cors_context.add_to_response(response))
}

pub async fn get_subscribed_labours(
    _req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user: User,
) -> worker::Result<Response> {
    let subscriptions = ctx
        .data
        .subscription_status_query
        .get_by_user_id(user.user_id)
        .await
        .map_err(|e| format!("Failed to query subscription status: {e}"))?;

    let labour_ids: Vec<_> = subscriptions.iter().map(|s| s.labour_id).collect();

    let labours = ctx
        .data
        .labour_status_query
        .get_by_ids(labour_ids)
        .await
        .map_err(|e| format!("Failed to query labour status: {e}"))?;

    let response = Response::from_json(&labours)
        .map_err(|e| format!("Failed to serialize response: {e}"))?;

    Ok(cors_context.add_to_response(response))
}
