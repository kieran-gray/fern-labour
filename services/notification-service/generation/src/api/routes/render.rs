use chrono::Utc;
use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::{
    InternalCommand, QueueMessage,
    service_clients::{RenderRequest, RenderResponse},
};
use tracing::{error, info};
use uuid::Uuid;
use worker::{Request, Response, RouteContext};

use crate::setup::app_state::AppState;

pub async fn render_async(
    mut req: Request,
    ctx: RouteContext<AppState>,
    service_id: String,
) -> worker::Result<Response> {
    let request: RenderRequest = match req.json().await {
        Ok(r) => r,
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to parse render request");
            return Response::error("Failed to parse render request", 400);
        }
    };

    info!(
        service_id = %service_id,
        channel = %request.channel,
        "Rendering notification template"
    );

    match ctx
        .data
        .template_engine
        .render_content(request.channel, request.template_data)
    {
        Ok(rendered_content) => {
            info!(service_id = %service_id, "Template rendered successfully");
            let command = InternalCommand::StoreRenderedContent {
                notification_id: request.notification_id,
                rendered_content,
            };
            let envelope = CommandEnvelope::enrich(
                QueueMessage::Internal(command),
                request.notification_id,
                Uuid::now_v7(),
                Uuid::now_v7(),
                "generation".to_string(),
                Utc::now(),
            );
            match ctx.data.command_producer.publish(envelope).await {
                Ok(_) => info!("PUBLISHED"),
                Err(e) => error!("FAILED: {e}"),
            }
            Response::empty()
        }
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to render template");
            Response::error(format!("Failed to render template: {e}"), 500)
        }
    }
}

pub async fn render(
    mut req: Request,
    ctx: RouteContext<AppState>,
    service_id: String,
) -> worker::Result<Response> {
    let request: RenderRequest = match req.json().await {
        Ok(r) => r,
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to parse render request");
            return Response::error("Failed to parse render request", 400);
        }
    };

    info!(
        service_id = %service_id,
        channel = %request.channel,
        "Rendering notification template"
    );

    match ctx
        .data
        .template_engine
        .render_content(request.channel, request.template_data)
    {
        Ok(rendered_content) => {
            info!(service_id = %service_id, "Template rendered successfully");
            Response::from_json(&RenderResponse { rendered_content })
        }
        Err(e) => {
            error!(service_id = %service_id, error = ?e, "Failed to render template");
            Response::error(format!("Failed to render template: {e}"), 500)
        }
    }
}
