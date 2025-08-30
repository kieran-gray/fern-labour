use std::time::Duration;

use crate::setup::app_state::AppState;

use super::{
    exception_handler::handle_error,
    routes::{admin::admin_router, events::events_router},
};
use http_body_util::BodyExt;

use axum::{
    Router,
    body::{Body, Bytes},
    error_handling::HandleErrorLayer,
    extract::Request,
    http::{HeaderValue, Method, Response, StatusCode},
    middleware::{self, Next},
    response::IntoResponse,
};

use tower::ServiceBuilder;
use tower_http::cors::CorsLayer;

pub fn create_router(state: AppState) -> Router {
    let cors = CorsLayer::new()
        .allow_origin("http://localhost:3000".parse::<HeaderValue>().unwrap())
        .allow_methods([Method::GET, Method::POST, Method::PATCH, Method::DELETE])
        .allow_credentials(true);

    let middleware_stack = ServiceBuilder::new()
        .layer(HandleErrorLayer::new(handle_error))
        .timeout(Duration::from_secs(1800))
        .layer(cors)
        .layer(middleware::from_fn(print_request_response));

    let app_routes = Router::new()
        .merge(admin_router())
        .nest("/events", events_router());

    Router::new()
        .nest("/api/v1", app_routes)
        .fallback(fallback)
        .layer(middleware_stack)
        .with_state(state)
}

async fn fallback() -> (StatusCode, &'static str) {
    (StatusCode::NOT_FOUND, "Not Found")
}

async fn print_request_response(
    req: Request,
    next: Next,
) -> Result<impl IntoResponse, (StatusCode, String)> {
    let (parts, body) = req.into_parts();
    let bytes = buffer_and_print("request", body).await?;
    let req = Request::from_parts(parts, Body::from(bytes));

    let res = next.run(req).await;

    let (parts, body) = res.into_parts();
    let bytes = buffer_and_print("response", body).await?;
    let res = Response::from_parts(parts, Body::from(bytes));

    Ok(res)
}

async fn buffer_and_print<B>(direction: &str, body: B) -> Result<Bytes, (StatusCode, String)>
where
    B: axum::body::HttpBody<Data = Bytes>,
    B::Error: std::fmt::Display,
{
    let bytes = match body.collect().await {
        Ok(collected) => collected.to_bytes(),
        Err(err) => {
            return Err((
                StatusCode::BAD_REQUEST,
                format!("failed to read {direction} body: {err}"),
            ));
        }
    };

    if let Ok(body) = std::str::from_utf8(&bytes) {
        tracing::debug!("{direction} body = {body:?}");
    }

    Ok(bytes)
}
