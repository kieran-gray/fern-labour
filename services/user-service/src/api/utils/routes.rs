use tracing::info;
use worker::{Request, Response, Result, RouteContext};

use crate::setup::app_state::AppState;

use fern_labour_workers_shared::{User, cors::CorsContext};

pub async fn authenticated<F, Fut>(
    handler: F,
    req: Request,
    ctx: RouteContext<AppState>,
) -> Result<Response>
where
    F: Fn(Request, RouteContext<AppState>, CorsContext, User) -> Fut,
    Fut: std::future::Future<Output = Result<Response>>,
{
    let cors_context = CorsContext::new(ctx.data.config.allowed_origins.clone(), &req);
    if let Err(response) = cors_context.validate(&req) {
        return Ok(response);
    }

    let user = if ctx.data.config.auth_enabled {
        let authorization = match req.headers().get("Authorization").ok().flatten() {
            Some(auth_header) => auth_header,
            None => {
                let response = Response::error("Unauthorised: Not Authenticated".to_string(), 401)?;
                return Ok(cors_context.add_to_response(response));
            }
        };
        match ctx.data.auth_service.authenticate(&authorization).await {
            Ok(user) => user,
            Err(e) => {
                info!(error = ?e, "User verification failed");
                let response =
                    Response::error("Unauthorised: User verification failed".to_string(), 404)?;
                return Ok(cors_context.add_to_response(response));
            }
        }
    } else {
        User {
            user_id: "anonymous".to_string(),
            issuer: "none".to_string(),
            email: None,
            email_verified: None,
            name: None,
        }
    };

    handler(req, ctx, cors_context, user).await
}

pub async fn public<F, Fut>(
    handler: F,
    req: Request,
    ctx: RouteContext<AppState>,
) -> Result<Response>
where
    F: Fn(Request, RouteContext<AppState>, CorsContext) -> Fut,
    Fut: std::future::Future<Output = Result<Response>>,
{
    let cors_context = CorsContext::new(ctx.data.config.allowed_origins.clone(), &req);
    if let Err(response) = cors_context.validate(&req) {
        return Ok(response);
    }

    handler(req, ctx, cors_context).await
}
