use axum::{Json, Router, extract::State, response::IntoResponse, routing::post};
use base64::prelude::*;

use crate::{
    api::schemas::requests::PubSubEvent,
    application::{dtos::event::Event, exceptions::AppError},
    setup::app_state::AppState,
};

pub fn extract_subscription_key(subscription_path: &str) -> Result<&str, AppError> {
    match subscription_path.split('/').collect::<Vec<&str>>().last() {
        Some(key) => return Ok(*key),
        _ => return Err(AppError::InvalidSubscription(subscription_path.to_string())),
    }
}

pub fn serialize_pub_sub_event(payload: PubSubEvent) -> Result<Event, AppError> {
    let event_data = match BASE64_STANDARD.decode(payload.message.data) {
        Ok(event_data_bytes) => match String::from_utf8(event_data_bytes) {
            Ok(event_data) => event_data,
            Err(_) => return Err(AppError::InvalidEventBody(payload.message.message_id)),
        },
        Err(_) => return Err(AppError::InvalidEventBody(payload.message.message_id)),
    };

    match serde_json::from_str(&event_data) {
        Ok(data) => return Ok(data),
        Err(err) => return Err(AppError::InvalidEventBody(err.to_string())),
    };
}

pub async fn event_handler(
    State(state): State<AppState>,
    Json(payload): Json<PubSubEvent>,
) -> Result<impl IntoResponse, AppError> {
    let subscription_key = extract_subscription_key(&payload.subscription)?;
    if subscription_key != "notification.requested.sub" {
        return Err(AppError::InvalidSubscription(String::from(
            subscription_key,
        )));
    }

    let event_data = serialize_pub_sub_event(payload)?;
    let event_body = event_data.data;

    let notification = state
        .notification_service
        .create_notification(
            event_body.channel,
            event_body.destination,
            event_body.template,
            event_body.data,
            event_body.metadata,
            None,
        )
        .await?;
    Ok(Json(notification))
}

pub fn events_router() -> Router<AppState> {
    Router::new().route("/handle", post(event_handler))
}
