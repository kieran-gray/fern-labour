use axum::{Json, response::IntoResponse};

pub mod router;

async fn health_check_handler() -> impl IntoResponse {
    let response = serde_json::json!({"status": "ok"});
    Json(response)
}
