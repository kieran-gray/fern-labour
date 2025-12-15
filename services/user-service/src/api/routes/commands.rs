use crate::{
    api::schemas::requests::{CreateUserRequest, UpdateUserRequest},
    application::exceptions::AppError,
    setup::app_state::AppState,
};
use fern_labour_workers_shared::{CorsContext, User};
use tracing::{error, info};
use worker::{Request, Response, RouteContext};

pub async fn create_user_handler(
    mut req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    _user: User,
) -> worker::Result<Response> {
    let payload: CreateUserRequest = match req.json().await {
        Ok(p) => p,
        Err(e) => {
            error!("Failed to parse request body: {:?}", e);
            let response = Response::from(AppError::ValidationError(
                "Failed to parse request body".into(),
            ));
            return Ok(cors_context.add_to_response(response));
        }
    };

    let app_payload = crate::application::dtos::CreateUserRequest {
        user_id: payload.user_id,
        email: payload.email,
        first_name: payload.first_name,
        last_name: payload.last_name,
        phone_number: payload.phone_number,
    };

    match ctx.data.user_command_service.create_user(app_payload).await {
        Ok(_) => {
            info!("User created successfully.");
            let response = Response::from_json(&serde_json::json!({
                "success": true,
                "message": "User created successfully"
            }))?;
            Ok(cors_context.add_to_response(response))
        }
        Err(e) => {
            error!("Failed to create user: {:?}", e);
            let response = Response::from(e);
            Ok(cors_context.add_to_response(response))
        }
    }
}

/// Update user profile
pub async fn update_user_handler(
    mut req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user: User,
) -> worker::Result<Response> {
    let payload: UpdateUserRequest = match req.json().await {
        Ok(p) => p,
        Err(e) => {
            error!("Failed to parse request body: {:?}", e);
            let response = Response::from(AppError::ValidationError(
                "Failed to parse request body".into(),
            ));
            return Ok(cors_context.add_to_response(response));
        }
    };

    let app_payload = crate::application::dtos::UpdateUserRequest {
        first_name: payload.first_name,
        last_name: payload.last_name,
        phone_number: payload.phone_number,
    };

    match ctx
        .data
        .user_command_service
        .update_user(user.user_id.clone(), app_payload)
        .await
    {
        Ok(_) => {
            info!(user_id = %user.user_id, "User profile updated successfully.");
            let response = Response::from_json(&serde_json::json!({
                "success": true,
                "message": "Profile updated successfully"
            }))?;
            Ok(cors_context.add_to_response(response))
        }
        Err(e) => {
            error!(user_id = %user.user_id, "Failed to update user: {:?}", e);
            let response = Response::from(e);
            Ok(cors_context.add_to_response(response))
        }
    }
}

/// Delete user (GDPR compliance)
pub async fn delete_user_handler(
    _req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user: User,
) -> worker::Result<Response> {
    match ctx
        .data
        .user_command_service
        .delete_user(user.user_id.clone())
        .await
    {
        Ok(_) => {
            info!(user_id = %user.user_id, "User deleted successfully.");
            let response = Response::from_json(&serde_json::json!({
                "success": true,
                "message": "User deleted successfully"
            }))?;
            Ok(cors_context.add_to_response(response))
        }
        Err(e) => {
            error!(user_id = %user.user_id, "Failed to delete user: {:?}", e);
            let response = Response::from(e);
            Ok(cors_context.add_to_response(response))
        }
    }
}
