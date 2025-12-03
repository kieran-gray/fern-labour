use serde_json::json;
use worker::{Request, Response, Result, RouteContext};

use crate::setup::app_state::AppState;

pub async fn with_service_id<F, Fut>(
    handler: F,
    req: Request,
    ctx: RouteContext<AppState>,
) -> Result<Response>
where
    F: Fn(Request, RouteContext<AppState>, String) -> Fut,
    Fut: std::future::Future<Output = Result<Response>>,
{
    let service_id = match req.headers().get("X-Service-ID").ok().flatten() {
        Some(service_header) => service_header,
        None => {
            return Response::from_json(&json!({
                "error": "Missing X-Service-ID header"
            }))
            .map(|r| r.with_status(401));
        }
    };

    handler(req, ctx, service_id).await
}
