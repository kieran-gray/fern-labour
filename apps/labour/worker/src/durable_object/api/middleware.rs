use fern_labour_workers_shared::clients::worker_clients::auth::User;
use tracing::error;
use worker::{Request, Response, Result};

use crate::durable_object::api::router::RequestContext;

pub async fn with_auth_context<'a, F, Fut>(
    handler: F,
    req: Request,
    ctx: RequestContext<'a>,
) -> Result<Response>
where
    F: Fn(Request, RequestContext<'a>, User) -> Fut,
    Fut: std::future::Future<Output = Result<Response>>,
{
    let headers = req.headers();

    let user_json = headers
        .get("X-User-Info")?
        .ok_or_else(|| worker::Error::RustError("Missing X-User-Info header".into()))?;

    let user: User = serde_json::from_str(&user_json)
        .map_err(|e| worker::Error::RustError(format!("Invalid user info: {}", e)))?;

    if let Err(e) = ctx
        .data
        .write_model()
        .user_storage
        .save_user_if_not_exists(&user)
    {
        error!(error = %e, user_id = %user.user_id, "Failed to save user");
    }

    handler(req, ctx, user).await
}
