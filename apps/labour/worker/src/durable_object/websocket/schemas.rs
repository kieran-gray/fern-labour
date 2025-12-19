use fern_labour_labour_shared::ApiCommand;
use tracing::error;
use worker::{Result, WebSocketIncomingMessage};

pub fn parse_websocket_message(message: WebSocketIncomingMessage) -> Result<ApiCommand> {
    let message: ApiCommand = match message {
        WebSocketIncomingMessage::String(data) => match serde_json::from_str(&data) {
            Ok(cmd) => cmd,
            Err(e) => {
                error!(error = ?e, message = %data, "Failed to parse ApiCommand from WebSocket message");
                return Err(worker::Error::RustError(format!(
                    "Failed to parse ApiCommand: {e}"
                )));
            }
        },
        WebSocketIncomingMessage::Binary(data) => match serde_json::from_slice(&data) {
            Ok(cmd) => cmd,
            Err(e) => {
                error!(error = ?e, "Failed to parse ApiCommand from WebSocket message");
                return Err(worker::Error::RustError(format!(
                    "Failed to parse ApiCommand: {e}"
                )));
            }
        },
    };
    Ok(message)
}
