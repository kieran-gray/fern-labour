use axum::{
    Router,
    routing::{get, post},
};

use super::health_check_handler;

pub fn create_router() -> Router {
    let twilio_routes = Router::new().route("/message-status", post(root));

    let event_routes = Router::new().route("/handle", post(root));

    let app_routes = Router::new()
        .route("/health", get(health_check_handler))
        .nest("/twilio", twilio_routes)
        .nest("/events", event_routes);

    Router::new().nest("/api/v1", app_routes)
}

async fn root() -> &'static str {
    "Hello, World!"
}
