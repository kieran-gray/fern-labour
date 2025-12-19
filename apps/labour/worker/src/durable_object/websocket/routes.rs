use fern_labour_labour_shared::ApiCommand;
use fern_labour_workers_shared::User;
use tracing::{info, warn};
use worker::{Request, Response, Result, State, WebSocketPair};

use crate::durable_object::{
    api::middleware::extract_auth_context, state::AggregateServices,
    write_side::domain::LabourCommand,
};

pub async fn upgrade_connection(req: Request, state: &State) -> Result<Response> {
    let user = extract_auth_context(&req)?;

    info!("Connecting websocket for {}", user.user_id);

    let WebSocketPair { client, server } = WebSocketPair::new()?;
    state.accept_web_socket(&server);

    server.serialize_attachment(&user).map_err(|e| {
        warn!("{}", e);
        worker::Error::RustError("Failure adding attachment to websocket connection".to_string())
    })?;

    Response::from_websocket(client)
}

pub fn handle_websocket_command(
    services: &AggregateServices,
    command: ApiCommand,
    user: User,
) -> anyhow::Result<()> {
    let domain_command = match command {
        ApiCommand::Admin(_) => {
            return Err(anyhow::anyhow!(
                "Admin commands not supported via WebSocket"
            ));
        }
        ApiCommand::Labour(cmd) => LabourCommand::from(cmd),
        ApiCommand::LabourUpdate(cmd) => LabourCommand::from(cmd),
        ApiCommand::Contraction(cmd) => LabourCommand::from(cmd),
        ApiCommand::Subscriber(cmd) => LabourCommand::from((cmd, user.user_id.clone())),
        ApiCommand::Subscription(cmd) => LabourCommand::from(cmd),
    };

    services
        .write_model()
        .labour_command_processor
        .handle_command(domain_command, user)
}
