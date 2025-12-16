use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_labour_shared::{
    AdminCommand, ContractionCommand, ContractionQuery, LabourCommand, LabourQuery,
    LabourUpdateCommand, LabourUpdateQuery, SubscriberCommand, SubscriptionCommand,
    queries::{subscription::SubscriptionQuery, user::UserQuery},
};
use fern_labour_workers_shared::clients::worker_clients::auth::User;
use tracing::info;
use worker::{Request, Response, Result};

use crate::durable_object::write_side::domain::LabourCommand as LabourDomainCommand;

#[derive(Debug, Clone)]
pub struct AuthContext {
    pub user: User,
}

pub enum RequestDto {
    DomainCommand {
        envelope: CommandEnvelope<LabourDomainCommand>,
        auth: AuthContext,
    },
    LabourCommand {
        envelope: CommandEnvelope<LabourCommand>,
        auth: AuthContext,
    },
    ContractionCommand {
        envelope: CommandEnvelope<ContractionCommand>,
        auth: AuthContext,
    },
    LabourUpdateCommand {
        envelope: CommandEnvelope<LabourUpdateCommand>,
        auth: AuthContext,
    },
    SubscriberCommand {
        envelope: CommandEnvelope<SubscriberCommand>,
        auth: AuthContext,
    },
    SubscriptionCommand {
        envelope: CommandEnvelope<SubscriptionCommand>,
        auth: AuthContext,
    },
    AdminCommand {
        envelope: CommandEnvelope<AdminCommand>,
        auth: AuthContext,
    },
    EventsQuery {
        auth: AuthContext,
    },
    UserQuery {
        query: UserQuery,
        auth: AuthContext,
    },
    LabourQuery {
        query: LabourQuery,
        auth: AuthContext,
    },
    ContractionQuery {
        query: ContractionQuery,
        auth: AuthContext,
    },
    LabourUpdateQuery {
        query: LabourUpdateQuery,
        auth: AuthContext,
    },
    SubscriptionQuery {
        query: SubscriptionQuery,
        auth: AuthContext,
    },
}

impl RequestDto {
    fn extract_auth_context(req: &Request) -> Result<AuthContext> {
        let headers = req.headers();

        let user_json = headers
            .get("X-User-Info")?
            .ok_or_else(|| worker::Error::RustError("Missing X-User-Info header".into()))?;

        let user: User = serde_json::from_str(&user_json)
            .map_err(|e| worker::Error::RustError(format!("Invalid user info: {}", e)))?;

        Ok(AuthContext { user })
    }

    pub fn auth_context(&self) -> &AuthContext {
        match self {
            RequestDto::DomainCommand { auth, .. } => auth,
            RequestDto::LabourCommand { auth, .. } => auth,
            RequestDto::ContractionCommand { auth, .. } => auth,
            RequestDto::LabourUpdateCommand { auth, .. } => auth,
            RequestDto::SubscriberCommand { auth, .. } => auth,
            RequestDto::SubscriptionCommand { auth, .. } => auth,
            RequestDto::AdminCommand { auth, .. } => auth,
            RequestDto::EventsQuery { auth } => auth,
            RequestDto::LabourQuery { auth, .. } => auth,
            RequestDto::ContractionQuery { auth, .. } => auth,
            RequestDto::LabourUpdateQuery { auth, .. } => auth,
            RequestDto::SubscriptionQuery { auth, .. } => auth,
            RequestDto::UserQuery { auth, .. } => auth,
        }
    }

    pub async fn from_request(mut req: Request) -> Result<Self> {
        let auth = Self::extract_auth_context(&req)?;

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

                Ok(Self::DomainCommand { envelope, auth })
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

                Ok(Self::LabourCommand { envelope, auth })
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

                Ok(Self::ContractionCommand { envelope, auth })
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

                Ok(Self::LabourUpdateCommand { envelope, auth })
            }
            (worker::Method::Post, "/subscription/command") => {
                let envelope: CommandEnvelope<SubscriptionCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized labour update command"
                );

                Ok(Self::SubscriptionCommand { envelope, auth })
            }
            (worker::Method::Post, "/subscriber/command") => {
                let envelope: CommandEnvelope<SubscriberCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    idempotency_key = %envelope.metadata.idempotency_key,
                    "Deserialized labour update command"
                );

                Ok(Self::SubscriberCommand { envelope, auth })
            }
            (worker::Method::Post, "/admin/command") => {
                let envelope: CommandEnvelope<AdminCommand> = req.json().await?;

                info!(
                    aggregate_id = %envelope.metadata.aggregate_id,
                    correlation_id = %envelope.metadata.correlation_id,
                    user_id = %envelope.metadata.user_id,
                    "Deserialized admin command"
                );

                Ok(Self::AdminCommand { envelope, auth })
            }
            (worker::Method::Get, "/labour/events") => Ok(Self::EventsQuery { auth }),
            (worker::Method::Post, "/labour/query") => {
                let query: LabourQuery = req.json().await?;

                info!(
                    query = ?query,
                    "Deserialized labour query"
                );

                Ok(Self::LabourQuery { query, auth })
            }
            (worker::Method::Post, "/contraction/query") => {
                let query: ContractionQuery = req.json().await?;

                info!(
                    query = ?query,
                    "Deserialized contraction query"
                );

                Ok(Self::ContractionQuery { query, auth })
            }
            (worker::Method::Post, "/labour-update/query") => {
                let query: LabourUpdateQuery = req.json().await?;

                info!(
                    query = ?query,
                    "Deserialized labour update query"
                );

                Ok(Self::LabourUpdateQuery { query, auth })
            }
            (worker::Method::Post, "/subscription/query") => {
                let query: SubscriptionQuery = req.json().await?;
                info!(
                    query = ?query,
                    "Deserialized subscription query"
                );

                Ok(Self::SubscriptionQuery { query, auth })
            }
            (worker::Method::Post, "/user/query") => {
                let query: UserQuery = req.json().await?;
                info!(
                    query = ?query,
                    "Deserialized user query"
                );

                Ok(Self::UserQuery { query, auth })
            }
            _ => Response::error("Not Found", 404).map(|_| unreachable!()),
        }
    }
}
