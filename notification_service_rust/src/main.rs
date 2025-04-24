use axum::{
    body::{Body, Bytes},
    extract::Request,
    http::StatusCode,
    middleware::{self, Next},
    response::{IntoResponse, Response},
    routing::{get, post},
    Router,
    Json,
};
use serde::Serialize;
use http_body_util::BodyExt;

const DOC_URL: &str = "/swagger/openapi.json";

async fn fallback() -> (StatusCode, &'static str) {
    (StatusCode::NOT_FOUND, "Not Found")
}

#[derive(Serialize)]
struct HealthCheck {
    status: String
}

#[tokio::main]
async fn main() {
    let twilio_routes = Router::new()
        .route("/message-status", post(root));

    let event_routes = Router::new()
        .route("/handle", post(root));

    let app_routes = Router::new()
        .route("/health", get(healthcheck))
        .nest("/twilio", twilio_routes)
        .nest("/events", event_routes);

    let app = Router::new()
        .route(DOC_URL, get(|| async { include_str!("openapi.json") }))
        .nest("/api/v1", app_routes)
        .layer(middleware::from_fn(print_request_response))
        .fallback(fallback);

    let listener = tokio::net::TcpListener::bind("127.0.0.1:8002")
        .await
        .unwrap();

    println!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
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
        println!("{direction} body = {body:?}");
    }

    Ok(bytes)
}

async fn root() -> &'static str {
    "Hello, World!"
}

async fn healthcheck() -> Json<HealthCheck> {
    let h = HealthCheck {
        status: String::from("ok")
    };
    Json(h)
}


