pub mod api;
pub mod exceptions;
pub mod read_side;
pub mod state;
pub mod token_generator;
pub mod write_side;

use tracing::{error, info};
use worker::{DurableObject, Env, Request, Response, Result, State, durable_object};

use crate::durable_object::{
    api::RequestDto, exceptions::IntoWorkerResponse, state::AggregateServices,
    write_side::infrastructure::alarm_manager::AlarmManager,
};

#[durable_object]
pub struct LabourAggregate {
    _state: State,
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
            _state: state,
            _env: env,
            services,
            alarm_manager,
        }
    }

    async fn fetch(&self, req: Request) -> Result<Response> {
        let request_dto = match RequestDto::from_request(req).await {
            Ok(dto) => dto,
            Err(err) => return Response::error(format!("Bad request: {}", err), 400),
        };

        let result = api::route_and_handle(self, request_dto);

        if result.is_success() && result.response().status_code() == 204 {
            // Only run alarm for empty responses, so we only run it when handling a
            // write-side command request.
            self.alarm_manager
                .set_alarm(0)
                .await
                .map_err(|e| worker::Error::RustError(e.to_string()))?;
        }

        Ok(result.into_response())
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
}
