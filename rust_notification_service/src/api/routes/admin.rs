use axum::{Json, Router, response::IntoResponse, routing::get};

use crate::setup::app_state::AppState;

pub async fn health_check_handler() -> impl IntoResponse {
    let response = serde_json::json!({"status": "ok"});
    Json(response)
}

pub fn admin_router() -> Router<AppState> {
    Router::new().route("/health", get(health_check_handler))
}
