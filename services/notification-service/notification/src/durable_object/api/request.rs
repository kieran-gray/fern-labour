use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::{AdminCommand, InternalCommand};
use tracing::info;
use worker::{Request, Response, Result};

use crate::durable_object::write_side::domain::NotificationCommand;

pub enum RequestDto {
    DomainCommand {
        envelope: CommandEnvelope<NotificationCommand>,
    },
    InternalCommand {
        envelope: CommandEnvelope<InternalCommand>,
    },
    AdminCommand {
        envelope: CommandEnvelope<AdminCommand>,
    },
    EventsQuery,
}

impl RequestDto {
    pub async fn from_request(mut req: Request) -> Result<Self> {
        let url = req.url()?;
        let path = url.path();
        let method = req.method();

        match (method, path) {
            (worker::Method::Post, "/notification/domain") => {
                let envelope: CommandEnvelope<NotificationCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized domain command"
                );

                Ok(Self::DomainCommand { envelope })
            }
            (worker::Method::Post, "/notification/command") => {
                let envelope: CommandEnvelope<InternalCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized internal command"
                );

                Ok(Self::InternalCommand { envelope })
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
            (worker::Method::Get, "/notification/events") => Ok(Self::EventsQuery),
            _ => Response::error("Not Found", 404).map(|_| unreachable!()),
        }
    }
}
