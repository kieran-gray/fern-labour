use fern_labour_workers_shared::clients::worker_clients::auth::User;
use tracing::error;
use worker::{Result, WebSocket};

pub fn extract_auth_context_from_websocket(ws: &WebSocket) -> Result<User> {
    let user: User = match ws.deserialize_attachment() {
        Ok(Some(user)) => user,
        Ok(None) => {
            let error = "No user found from WebSocket attachment";
            error!(error);
            return Err(worker::Error::RustError(error.to_string()));
        }
        Err(e) => {
            let error = format!("Failed to deserialize user from WebSocket attachment: {e}");
            error!(error);
            return Err(worker::Error::RustError(error));
        }
    };
    Ok(user)
}
