pub mod api;
pub mod exceptions;
pub mod read_side;
pub mod security;
pub mod state;
pub mod user_storage;
pub mod write_side;

use tracing::{error, info, warn};
use worker::{
    DurableObject, Env, Request, Response, Result, State, WebSocket, WebSocketIncomingMessage,
    WebSocketPair, durable_object,
};

use crate::durable_object::{
    api::{middleware::extract_auth_context, router::route_request},
    exceptions::IntoWorkerResponse,
    state::AggregateServices,
    write_side::infrastructure::alarm_manager::AlarmManager,
};

#[durable_object]
pub struct LabourAggregate {
    state: State,
    _env: Env,
    pub(crate) services: AggregateServices,
    alarm_manager: AlarmManager,
}

impl DurableObject for LabourAggregate {
    fn new(state: State, env: Env) -> Self {
        let services = match AggregateServices::from_worker_state(&state, &env) {
            Ok(s) => s,
            Err(err) => panic!("{}", err),
        };

        let alarm_manager = AlarmManager::create(state.storage());

        Self {
            state,
            _env: env,
            services,
            alarm_manager,
        }
    }

    async fn fetch(&self, req: Request) -> Result<Response> {
        if req.path().contains("/websocket") {
            return self.handle_websocket_command(req).await;
        }

        let result = route_request(req, &self.services).await?;

        if result.status_code() == 204 {
            // Only run alarm for empty responses, so we only run it when handling a
            // write-side command request.
            self.alarm_manager
                .set_alarm(0)
                .await
                .map_err(|e| worker::Error::RustError(e.to_string()))?;
        }

        Ok(result)
    }

    async fn alarm(&self) -> Result<Response> {
        info!("Alarm triggered - processing async operations");
        let alarm_services = self.services.async_processors();

        let sync_result = alarm_services
            .sync_projection_processor
            .process_projections();

        if let Err(e) = sync_result {
            error!(error = %e, "Error in sync projection processing");
        }

        let async_result = alarm_services
            .async_projection_processor
            .process_projections()
            .await;

        match async_result {
            Ok(_) => {
                info!("All async operations completed successfully");
                Response::empty()
            }
            Err(e) => {
                error!(error = %e, "Error in async processing");
                Ok(e.into_response())
            }
        }
    }

    async fn websocket_message(
        &self,
        _ws: WebSocket,
        message: WebSocketIncomingMessage,
    ) -> Result<()> {
        match message {
            WebSocketIncomingMessage::String(str_data) => {
                info!(str_data)
            }
            WebSocketIncomingMessage::Binary(binary_data) => {
                dbg!("{:?}", binary_data);
            }
        };
        Ok(())
    }

    async fn websocket_close(
            &self,
            _ws: WebSocket,
            _code: usize,
            _reason: String,
            _was_clean: bool,
        ) -> Result<()> {
        info!("Client disconnected");
        Ok(())
    }
}

impl LabourAggregate {
    async fn handle_websocket_command(&self, req: Request) -> Result<Response> {
        let user = extract_auth_context(&req)?;

        info!("Connecting websocket for {}", user.user_id);

        let WebSocketPair { client, server } = WebSocketPair::new()?;
        self.state.accept_web_socket(&server);

        server.serialize_attachment(&user).map_err(|e| {
            warn!("{}", e);
            worker::Error::RustError(
                "Failure adding attachment to websocket connection".to_string(),
            )
        })?;

        let events = self
            .services
            .read_model()
            .event_query
            .get_event_stream()
            .map_err(|_| worker::Error::RustError("Failed to fetch event stream".to_string()))?;

        server.send(&events).unwrap_or(());

        Response::from_websocket(client)
    }
}
