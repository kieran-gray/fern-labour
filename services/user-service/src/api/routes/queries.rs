use crate::{application::exceptions::AppError, setup::app_state::AppState};
use fern_labour_workers_shared::{CorsContext, User};
use tracing::{error, info};
use worker::{Request, Response, RouteContext};

pub async fn get_current_user(
    _req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user: User,
) -> worker::Result<Response> {
    match ctx
        .data
        .user_query_service
        .get_user_by_id(user.user_id.clone())
        .await
    {
        Ok(user_dto) => {
            info!(user_id = %user.user_id, "Retrieved user profile successfully.");
            let response = Response::from_json(&user_dto)?;
            Ok(cors_context.add_to_response(response))
        }
        Err(e) => {
            error!(user_id = %user.user_id, "Failed to retrieve user: {:?}", e);
            let response = Response::from(e);
            Ok(cors_context.add_to_response(response))
        }
    }
}

pub async fn get_user_by_id(
    _req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user: User,
) -> worker::Result<Response> {
    let user_id = match ctx.param("user_id") {
        Some(id) => id.clone(),
        _ => {
            let error = "No user_id provided in path";
            error!(error);
            let response = Response::from(AppError::ValidationError(error.to_string()));
            return Ok(cors_context.add_to_response(response));
        }
    };

    if user_id != user.user_id {
        let error = "Unauthorized: You can only access your own profile";
        error!(requested_user_id = %user_id, authenticated_user_id = %user.user_id, error);
        let response = Response::from(AppError::Unauthorised(error.to_string()));
        return Ok(cors_context.add_to_response(response));
    }

    match ctx.data.user_query_service.get_user_by_id(user_id).await {
        Ok(user_dto) => {
            info!(user_id = %user.user_id, "Retrieved user profile successfully.");
            let response = Response::from_json(&user_dto)?;
            Ok(cors_context.add_to_response(response))
        }
        Err(e) => {
            error!(user_id = %user.user_id, "Failed to retrieve user: {:?}", e);
            let response = Response::from(e);
            Ok(cors_context.add_to_response(response))
        }
    }
}
