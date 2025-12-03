use chrono::Utc;
use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::{
    InternalCommand, QueueMessage,
    service_clients::{DispatchRequest, DispatchResponse},
};
use tracing::{error, info};
use uuid::Uuid;
use worker::{Request, Response, RouteContext};

use crate::{application::dispatch::DispatchContext, setup::app_state::AppState};

pub async fn dispatch_async(
    mut req: Request,
    ctx: RouteContext<AppState>,
    service_id: String,
) -> worker::Result<Response> {
    let dispatch_request: DispatchRequest = match req.json().await {
        Ok(r) => r,
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to parse dispatch request");
            return Response::error("Failed to parse dispatch request", 400);
        }
    };
    let notification_id = dispatch_request.notification_id;

    let context = DispatchContext::from(dispatch_request);

    info!(
        service_id = %service_id,
        channel = %context.channel(),
        destination = %context.destination,
        "Dispatching notification"
    );

    match ctx.data.notification_router.dispatch(context).await {
        Ok(external_id) => {
            info!("Notification dispatched successfully");
            let command = InternalCommand::MarkAsDispatched {
                notification_id,
                external_id,
            };
            let envelope = CommandEnvelope::enrich(
                QueueMessage::Internal(command),
                notification_id,
                Uuid::now_v7(),
                Uuid::now_v7(),
                "dispatch".to_string(),
                Utc::now(),
            );

            match ctx.data.command_producer.publish(envelope).await {
                Ok(_) => info!("PUBLISHED"),
                Err(e) => error!("FAILED: {e}"),
            }
            Response::empty()
        }
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to dispatch notification");
            Response::error(format!("Failed to dispatch notification: {e}"), 500)
        }
    }
}

pub async fn dispatch(
    mut req: Request,
    ctx: RouteContext<AppState>,
    service_id: String,
) -> worker::Result<Response> {
    let dispatch_request: DispatchRequest = match req.json().await {
        Ok(r) => r,
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to parse dispatch request");
            return Response::error("Failed to parse dispatch request", 400);
        }
    };

    let context = DispatchContext::from(dispatch_request);

    info!(
        service_id = %service_id,
        channel = %context.channel(),
        destination = %context.destination,
        "Dispatching notification"
    );

    match ctx.data.notification_router.dispatch(context).await {
        Ok(external_id) => {
            info!("Notification dispatched successfully");
            let response = DispatchResponse { external_id };
            Response::from_json(&response)
        }
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to dispatch notification");
            Response::error(format!("Failed to dispatch notification: {e}"), 500)
        }
    }
}
