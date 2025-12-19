pub mod api;
pub mod exceptions;
pub mod read_side;
pub mod security;
pub mod state;
pub mod websocket;
pub mod write_side;

use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{
    DurableObject, Env, Request, Response, Result, State, WebSocket, WebSocketIncomingMessage,
    durable_object,
};

use crate::durable_object::{
    api::router::route_request,
    exceptions::IntoWorkerResponse,
    state::AggregateServices,
    websocket::{
        middleware::extract_auth_context_from_websocket,
        routes::{handle_websocket_command, upgrade_connection},
        schemas::parse_websocket_message,
    },
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
        if req.path() == "/websocket" {
            return upgrade_connection(req, &self.state).await;
        }

        let result = route_request(req, &self.services).await?;

        if result.status_code() == 204 {
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

        let sequence_before = alarm_services
            .sync_projection_processor
            .get_last_processed_sequence();

        let sync_result = alarm_services
            .sync_projection_processor
            .process_projections();

        if let Err(e) = sync_result {
            error!(error = %e, "Error in sync projection processing");
        } else {
            // TODO race condition for labour and subscription read models that project to D1
            let sequence_after = alarm_services
                .sync_projection_processor
                .get_last_processed_sequence();

            if sequence_after > sequence_before
                && let Err(e) = alarm_services
                    .websocket_event_broadcaster
                    .broadcast_new_events(&self.state, sequence_before)
            {
                error!(error = %e, "Failed to broadcast events to WebSocket clients");
            }
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
        ws: WebSocket,
        message: WebSocketIncomingMessage,
    ) -> Result<()> {
        let command = parse_websocket_message(message)?;
        let user: User = extract_auth_context_from_websocket(&ws)?;

        info!(user_id = %user.user_id, command = ?command, "Processing command from WebSocket");
        let result = handle_websocket_command(&self.services, command, user);

        if let Err(e) = result {
            error!(error = %e, "Command execution failed");
        } else {
            info!("Command executed successfully");

            if let Err(e) = self.alarm_manager.set_alarm(0).await {
                error!(error = %e, "Failed to set alarm after command");
            }
        }

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
