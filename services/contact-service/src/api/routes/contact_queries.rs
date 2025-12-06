use crate::setup::app_state::AppState;
use fern_labour_workers_shared::CorsContext;
use tracing::{debug, error};
use worker::{Request, Response, RouteContext};

pub async fn get_contact_messages_handler(
    req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user_id: String,
) -> worker::Result<Response> {
    let url = req.url()?;
    let query_pairs: Vec<(String, String)> = url
        .query_pairs()
        .map(|(k, v)| (k.to_string(), v.to_string()))
        .collect();

    let limit = query_pairs
        .iter()
        .find(|(k, _)| k == "limit")
        .and_then(|(_, v)| v.parse::<i64>().ok());

    let offset = query_pairs
        .iter()
        .find(|(k, _)| k == "offset")
        .and_then(|(_, v)| v.parse::<i64>().ok());

    let result = match (limit, offset) {
        (Some(l), Some(o)) => {
            debug!(user_id = ?user_id, limit = l, offset = o, "Fetching paginated contact messages");
            ctx.data
                .contact_message_query_service
                .get_messages_paginated(l, o)
                .await
        }
        _ => {
            debug!(user_id = ?user_id, "Fetching all contact messages");
            ctx.data.contact_message_query_service.get_messages().await
        }
    };

    match result {
        Ok(contact_messages) => {
            debug!(user_id = ?user_id, count = contact_messages.len(), "Contact Messages successfully fetched");
            let response = Response::from_json(&contact_messages)?;
            Ok(cors_context.add_to_response(response))
        }
        Err(e) => {
            error!(user_id = ?user_id, "Failed to get messages: {:?}", e);
            let response = Response::from(e);
            Ok(cors_context.add_to_response(response))
        }
    }
}

pub async fn get_contact_message_activity_handler(
    _req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user_id: String,
) -> worker::Result<Response> {
    let days: i64 = match ctx.param("days") {
        Some(id) => id
            .parse()
            .map_err(|_| format!("Invalid days param: {}", id))?,
        _ => {
            let error = "No days param provided in query";
            error!(user_id = %user_id, error);
            let response = Response::error(error, 400)?;
            return Ok(cors_context.add_to_response(response));
        }
    };

    match ctx
        .data
        .contact_message_query_service
        .get_activity(days)
        .await
    {
        Ok(activity) => {
            debug!(user_id = ?user_id, "Contact Message Activity successfully fetched");
            let response = Response::from_json(&activity)?;
            Ok(cors_context.add_to_response(response))
        }
        Err(e) => {
            error!(user_id = ?user_id, "Failed to get contact message activity: {:?}", e);
            let response = Response::from(e);
            Ok(cors_context.add_to_response(response))
        }
    }
}
