use tracing::{error, info};
use worker::Response;

use crate::durable_object::{
    NotificationAggregate, api::RequestDto, exceptions::IntoWorkerResponse,
    write_side::domain::LabourCommand,
};

pub enum CommandResult {
    Success(Response),
    Failed(Response),
}

impl CommandResult {
    pub fn into_response(self) -> Response {
        match self {
            CommandResult::Success(r) | CommandResult::Failed(r) => r,
        }
    }

    pub fn is_success(&self) -> bool {
        matches!(self, CommandResult::Success(_))
    }

    pub fn from_unit_result(result: anyhow::Result<()>) -> Self {
        match result {
            Ok(()) => Self::Success(Response::empty().unwrap()),
            Err(err) => Self::Failed(err.into_response()),
        }
    }

    pub fn from_json_result<T: serde::Serialize>(result: anyhow::Result<T>) -> Self {
        match result {
            Ok(data) => Self::Success(Response::from_json(&data).unwrap()),
            Err(err) => Self::Failed(err.into_response()),
        }
    }
}

pub fn route_and_handle(aggregate: &NotificationAggregate, request: RequestDto) -> CommandResult {
    match request {
        RequestDto::DomainCommand { envelope } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing domain command"
            );

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(envelope.command, envelope.metadata.user_id.clone());

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            CommandResult::from_unit_result(result)
        }
        RequestDto::LabourCommand { envelope } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing labour command"
            );

            let domain_command = LabourCommand::from(envelope.command.clone());

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, envelope.metadata.user_id.clone());

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            CommandResult::from_unit_result(result)
        }
        RequestDto::LabourUpdateCommand { envelope } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing labour update command"
            );

            let domain_command = LabourCommand::from(envelope.command.clone());

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, envelope.metadata.user_id.clone());

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            CommandResult::from_unit_result(result)
        }
        RequestDto::ContractionCommand { envelope } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing contraction command"
            );

            let domain_command = LabourCommand::from(envelope.command.clone());

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, envelope.metadata.user_id.clone());

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            CommandResult::from_unit_result(result)
        }
        RequestDto::AdminCommand { envelope } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                "Processing admin command"
            );

            let result = aggregate
                .services
                .write_model()
                .admin_command_processor
                .handle(envelope);

            if let Err(ref err) = result {
                error!("Admin command handling failed: {}", err);
            } else {
                info!("Admin command handled successfully");
            }

            CommandResult::from_unit_result(result)
        }
        RequestDto::EventsQuery => CommandResult::from_json_result(
            aggregate
                .services
                .read_model()
                .query_service
                .get_event_stream(),
        ),
    }
}
