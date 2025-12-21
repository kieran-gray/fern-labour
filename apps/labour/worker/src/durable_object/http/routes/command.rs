use fern_labour_labour_shared::ApiCommand;
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    http::{ApiResult, router::RequestContext},
    write_side::command_translator::CommandTranslator,
};

pub async fn handle_command(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let command: ApiCommand = match req.json().await {
        Ok(cmd) => cmd,
        Err(e) => {
            error!(error = ?e, "Failed to parse ApiCommand");
            return Response::error("Failed to parse request body", 400);
        }
    };

    info!(command = ?command, user_id = %user.user_id, "Processing command");

    let domain_command = match CommandTranslator::translate(command, &user) {
        Ok(cmd) => cmd,
        Err(e) => {
            error!(error = %e, "Command translation failed");
            return Response::error(e.to_string(), 400);
        }
    };

    let result = ctx
        .data
        .write_model()
        .labour_command_processor
        .handle_command(domain_command, user);

    if let Err(ref err) = result {
        error!(error = %err, "Command execution failed");
    } else {
        info!("Command executed successfully");
    }

    Ok(ApiResult::from_unit_result(result).into_response())
}
