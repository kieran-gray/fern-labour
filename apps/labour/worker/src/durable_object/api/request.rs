use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_labour_shared::{
    AdminCommand, ContractionCommand, ContractionQuery, LabourCommand, LabourQuery,
    LabourUpdateCommand, LabourUpdateQuery,
};
use tracing::info;
use worker::{Request, Response, Result};

use crate::durable_object::write_side::domain::LabourCommand as LabourDomainCommand;

pub enum RequestDto {
    DomainCommand {
        envelope: CommandEnvelope<LabourDomainCommand>,
    },
    LabourCommand {
        envelope: CommandEnvelope<LabourCommand>,
    },
    ContractionCommand {
        envelope: CommandEnvelope<ContractionCommand>,
    },
    LabourUpdateCommand {
        envelope: CommandEnvelope<LabourUpdateCommand>,
    },
    AdminCommand {
        envelope: CommandEnvelope<AdminCommand>,
    },
    EventsQuery,
    LabourQuery {
        query: LabourQuery,
    },
    ContractionQuery {
        query: ContractionQuery,
    },
    LabourUpdateQuery {
        query: LabourUpdateQuery,
    },
}

impl RequestDto {
    pub async fn from_request(mut req: Request) -> Result<Self> {
        let url = req.url()?;
        let path = url.path();
        let method = req.method();

        match (method, path) {
            (worker::Method::Post, "/labour/domain") => {
                let envelope: CommandEnvelope<LabourDomainCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized domain command"
                );

                Ok(Self::DomainCommand { envelope })
            }
            (worker::Method::Post, "/labour/command") => {
                let envelope: CommandEnvelope<LabourCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized labour command"
                );

                Ok(Self::LabourCommand { envelope })
            }
            (worker::Method::Post, "/contraction/command") => {
                let envelope: CommandEnvelope<ContractionCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized contraction command"
                );

                Ok(Self::ContractionCommand { envelope })
            }
            (worker::Method::Post, "/labour-update/command") => {
                let envelope: CommandEnvelope<LabourUpdateCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized labour update command"
                );

                Ok(Self::LabourUpdateCommand { envelope })
            }
            (worker::Method::Post, "/admin/command") => {
                let envelope: CommandEnvelope<AdminCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    "Deserialized admin command"
                );

                Ok(Self::AdminCommand { envelope })
            }
            (worker::Method::Get, "/labour/events") => Ok(Self::EventsQuery),
            (worker::Method::Post, "/labour/query") => {
                let query: LabourQuery = req.json().await?;

                info!(
                    query = ?query,
                    "Deserialized labour query"
                );

                Ok(Self::LabourQuery { query })
            }
            (worker::Method::Post, "/contraction/query") => {
                let query: ContractionQuery = req.json().await?;

                info!(
                    query = ?query,
                    "Deserialized contraction query"
                );

                Ok(Self::ContractionQuery { query })
            }
            (worker::Method::Post, "/labour-update/query") => {
                let query: LabourUpdateQuery = req.json().await?;

                info!(
                    query = ?query,
                    "Deserialized labour update query"
                );

                Ok(Self::LabourUpdateQuery { query })
            }
            _ => Response::error("Not Found", 404).map(|_| unreachable!()),
        }
    }
}
