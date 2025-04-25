use std::collections::HashMap;
use base64::prelude::*;
use axum::{Json, Router, extract::State, response::IntoResponse, routing::post};

use crate::{
    api::schemas::requests::PubSubEvent, application::exceptions::AppError,
    setup::app_state::AppState,
};

pub async fn event_handler(
    State(state): State<AppState>,
    Json(payload): Json<PubSubEvent>,
) -> Result<impl IntoResponse, AppError> {
    let subscription: &str = payload
        .subscription
        .split('/')
        .collect::<Vec<&str>>()
        .last()
        .expect("Invalid subscription key");
    if subscription != "notification.requested.sub" {
        return Err(AppError::InvalidSubscription(String::from(subscription)));
    }

    let event_data = match BASE64_STANDARD.decode(payload.message.data) {
        Ok(event_data_bytes) => {
            match String::from_utf8(event_data_bytes) {
                Ok(event_data) => event_data,
                Err(_) => return Err(AppError::InvalidEventBody(payload.message.message_id))
            }
        },
        Err(_) => return Err(AppError::InvalidEventBody(payload.message.message_id))
    };

    let mut data = HashMap::new();
    data.insert(String::from("update"), String::from("Baby on the way"));
    let notification = state
        .notification_service
        .create_notification(
            String::from("sms"),
            String::from("07123123123"),
            String::from("labour_update"),
            data,
            None,
            None,
        )
        .await?;
    Ok(Json(notification))
}

pub fn events_router() -> Router<AppState> {
    Router::new().route("/handle", post(event_handler))
}
