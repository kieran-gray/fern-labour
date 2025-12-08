use fern_labour_labour_shared::ApiCommand;
use fern_labour_workers_shared::CorsContext;
use tracing::error;
use worker::{Request, Response, RouteContext};

use crate::api_worker::{AppState, api::exceptions::ApiError};

pub async fn handle_command(
    mut req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user_id: String,
) -> worker::Result<Response> {
    let command: ApiCommand = match req.json().await {
        Ok(command) => command,
        Err(e) => {
            error!(user_id = %user_id, error = ?e, "Failed to parse request body");
            let response = Response::from(ApiError::ValidationError(
                "Failed to parse request body".into(),
            ));
            return Ok(cors_context.add_to_response(response));
        }
    };

    let labour_id = command.labour_id();

    let response = match command {
        ApiCommand::Admin(cmd) => ctx
            .data
            .do_client
            .command(labour_id, cmd, user_id, "/admin/command")
            .await
            .map_err(|e| format!("Failed to send command to labour aggregate: {e}"))?,
        ApiCommand::Labour(cmd) => ctx
            .data
            .do_client
            .command(labour_id, cmd, user_id, "/labour/command")
            .await
            .map_err(|e| format!("Failed to send command to labour aggregate: {e}"))?,
        ApiCommand::LabourUpdate(cmd) => ctx
            .data
            .do_client
            .command(labour_id, cmd, user_id, "/labour-update/command")
            .await
            .map_err(|e| format!("Failed to send command to labour aggregate: {e}"))?,
        ApiCommand::Contraction(cmd) => ctx
            .data
            .do_client
            .command(labour_id, cmd, user_id, "/contraction/command")
            .await
            .map_err(|e| format!("Failed to send command to labour aggregate: {e}"))?,
        ApiCommand::Subscriber(cmd) => ctx
            .data
            .do_client
            .command(labour_id, cmd, user_id, "/subscriber/command")
            .await
            .map_err(|e| format!("Failed to send command to labour aggregate: {e}"))?,
        ApiCommand::Subscription(cmd) => ctx
            .data
            .do_client
            .command(labour_id, cmd, user_id, "/subscription/command")
            .await
            .map_err(|e| format!("Failed to send command to labour aggregate: {e}"))?,
    };

    Ok(cors_context.add_to_response(response))
}
