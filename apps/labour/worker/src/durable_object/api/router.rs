use base64::{Engine, prelude::BASE64_URL_SAFE_NO_PAD};
use chrono::DateTime;
use fern_labour_event_sourcing_rs::{Cursor, DecodedCursor, PaginatedResponse};
use fern_labour_labour_shared::{
    ContractionQuery, LabourQuery, LabourUpdateQuery,
    queries::{subscription::SubscriptionQuery, user::UserQuery},
};
use tracing::{error, info};
use worker::Response;

use crate::durable_object::{
    LabourAggregate,
    api::RequestDto,
    exceptions::IntoWorkerResponse,
    read_side::read_models::{
        contractions::ContractionReadModelQueryHandler, labour::LabourReadModelQueryHandler,
        labour_updates::LabourUpdateReadModelQueryHandler,
        subscriptions::SubscriptionReadModelQueryHandler,
    },
    write_side::domain::LabourCommand,
};

pub enum ApiResult {
    Success(Response),
    Failed(Response),
}

impl ApiResult {
    pub fn into_response(self) -> Response {
        match self {
            ApiResult::Success(r) | ApiResult::Failed(r) => r,
        }
    }

    pub fn response(&self) -> &Response {
        match self {
            ApiResult::Success(r) | ApiResult::Failed(r) => r,
        }
    }

    pub fn is_success(&self) -> bool {
        matches!(self, ApiResult::Success(_))
    }

    pub fn from_unit_result(result: anyhow::Result<()>) -> Self {
        match result {
            Ok(()) => Self::Success(Response::empty().unwrap().with_status(204)),
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

pub fn route_and_handle(aggregate: &LabourAggregate, request: RequestDto) -> ApiResult {
    match request {
        RequestDto::DomainCommand { envelope, auth } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                auth_user_id = %auth.user.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing domain command"
            );

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(envelope.command, auth.user);

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            ApiResult::from_unit_result(result)
        }
        RequestDto::LabourCommand { envelope, auth } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                auth_user_id = %auth.user.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing labour command"
            );

            let domain_command = LabourCommand::from(envelope.command.clone());

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, auth.user);

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            ApiResult::from_unit_result(result)
        }
        RequestDto::LabourUpdateCommand { envelope, auth } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                auth_user_id = %auth.user.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing labour update command"
            );

            let domain_command = LabourCommand::from(envelope.command.clone());

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, auth.user);

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            ApiResult::from_unit_result(result)
        }
        RequestDto::ContractionCommand { envelope, auth } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                auth_user_id = %auth.user.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing contraction command"
            );

            let domain_command = LabourCommand::from(envelope.command.clone());

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, auth.user);

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            ApiResult::from_unit_result(result)
        }
        RequestDto::SubscriberCommand { envelope, auth } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                auth_user_id = %auth.user.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing subscriber command"
            );

            let domain_command =
                LabourCommand::from((envelope.command.clone(), auth.user.user_id.clone()));

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, auth.user);

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            ApiResult::from_unit_result(result)
        }
        RequestDto::SubscriptionCommand { envelope, auth } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                auth_user_id = %auth.user.user_id,
                idempotency_key = %envelope.metadata.idempotency_key,
                "Processing subscription command"
            );

            let domain_command = LabourCommand::from(envelope.command.clone());

            let result = aggregate
                .services
                .write_model()
                .labour_command_processor
                .handle_command(domain_command, auth.user);

            if let Err(ref err) = result {
                error!("Command execution failed: {}", err);
            } else {
                info!("Command executed successfully");
            }

            ApiResult::from_unit_result(result)
        }
        RequestDto::AdminCommand { envelope, auth } => {
            info!(
                aggregate_id = %envelope.metadata.aggregate_id,
                correlation_id = %envelope.metadata.correlation_id,
                user_id = %envelope.metadata.user_id,
                auth_user_id = %auth.user.user_id,
                "Processing admin command"
            );

            let result = aggregate
                .services
                .write_model()
                .admin_command_processor
                .handle(envelope, auth.user);

            if let Err(ref err) = result {
                error!("Admin command handling failed: {}", err);
            } else {
                info!("Admin command handled successfully");
            }

            ApiResult::from_unit_result(result)
        }
        RequestDto::EventsQuery { auth } => {
            info!(auth_user_id = %auth.user.user_id, "Processing events query");
            ApiResult::from_json_result(
                aggregate
                    .services
                    .read_model()
                    .event_query
                    .get_event_stream(),
            )
        }
        RequestDto::LabourQuery { query, auth } => {
            info!(query = ?query, auth_user_id = %auth.user.user_id, "Processing labour query");

            let result = match query {
                LabourQuery::GetLabour { labour_id } => {
                    info!(labour_id = %labour_id, "Getting labour");
                    aggregate.services.read_model().labour_query.get()
                }
            };

            if let Err(ref err) = result {
                error!("Query execution failed: {}", err);
            } else {
                info!("Query executed successfully");
            }

            ApiResult::from_json_result(result)
        }
        RequestDto::UserQuery { query, auth } => {
            info!(query = ?query, auth_user_id = %auth.user.user_id, "Processing user query");

            let result = match query {
                UserQuery::GetUser { labour_id, user_id } => {
                    info!(labour_id = %labour_id, user_id = %user_id, "Getting user");
                    aggregate
                        .services
                        .read_model()
                        .user_query
                        .get_user_by_id(user_id)
                }
                UserQuery::GetUsers { labour_id } => {
                    info!(labour_id = %labour_id, "Getting users");
                    aggregate.services.read_model().user_query.get_users()
                }
            };

            if let Err(ref err) = result {
                error!("Query execution failed: {}", err);
            } else {
                info!("Query executed successfully");
            }

            ApiResult::from_json_result(result)
        }
        RequestDto::ContractionQuery { query, auth } => {
            info!(query = ?query, auth_user_id = %auth.user.user_id, "Processing contraction query");

            let result = match query {
                ContractionQuery::GetContractions {
                    labour_id,
                    limit,
                    cursor,
                } => {
                    info!(labour_id = %labour_id, limit = %limit, "Getting contractions");
                    let decoded_cursor = cursor.map(|c| DecodedCursor {
                        last_id: c.id,
                        last_updated_at: DateTime::parse_from_rfc3339(&c.updated_at)
                            .map(|dt| dt.with_timezone(&chrono::Utc))
                            .unwrap_or_else(|_| chrono::Utc::now()),
                    });
                    aggregate
                        .services
                        .read_model()
                        .contraction_query
                        .get(limit + 1, decoded_cursor)
                        .map(|items| build_paginated_response(items, limit))
                }
                ContractionQuery::GetContractionById {
                    labour_id,
                    contraction_id,
                } => {
                    info!(labour_id = %labour_id, contraction_id = %contraction_id, "Getting contraction by ID");
                    aggregate
                        .services
                        .read_model()
                        .contraction_query
                        .get_by_id(contraction_id)
                        .map(|c| vec![c])
                        .map(|items| PaginatedResponse {
                            data: items,
                            next_cursor: None,
                            has_more: false,
                        })
                }
            };

            if let Err(ref err) = result {
                error!("Query execution failed: {}", err);
            } else {
                info!("Query executed successfully");
            }

            ApiResult::from_json_result(result)
        }
        RequestDto::LabourUpdateQuery { query, auth } => {
            info!(query = ?query, auth_user_id = %auth.user.user_id, "Processing labour update query");

            let result = match query {
                LabourUpdateQuery::GetLabourUpdates {
                    labour_id,
                    limit,
                    cursor,
                } => {
                    info!(labour_id = %labour_id, limit = %limit, "Getting labour updates");
                    let decoded_cursor = cursor.map(|c| DecodedCursor {
                        last_id: c.id,
                        last_updated_at: DateTime::parse_from_rfc3339(&c.updated_at)
                            .map(|dt| dt.with_timezone(&chrono::Utc))
                            .unwrap_or_else(|_| chrono::Utc::now()),
                    });
                    aggregate
                        .services
                        .read_model()
                        .labour_update_query
                        .get(limit + 1, decoded_cursor)
                        .map(|items| build_paginated_response(items, limit))
                }
                LabourUpdateQuery::GetLabourUpdateById {
                    labour_id,
                    labour_update_id,
                } => {
                    info!(labour_id = %labour_id, labour_update_id = %labour_update_id, "Getting labour update by ID");
                    aggregate
                        .services
                        .read_model()
                        .labour_update_query
                        .get_by_id(labour_update_id)
                        .map(|u| vec![u])
                        .map(|items| PaginatedResponse {
                            data: items,
                            next_cursor: None,
                            has_more: false,
                        })
                }
            };

            if let Err(ref err) = result {
                error!("Query execution failed: {}", err);
            } else {
                info!("Query executed successfully");
            }

            ApiResult::from_json_result(result)
        }
        RequestDto::SubscriptionQuery { query, auth } => {
            info!(query = ?query, auth_user_id = %auth.user.user_id, "Processing subscription query");

            match query {
                SubscriptionQuery::GetSubscriptionToken { labour_id } => {
                    info!(labour_id = %labour_id, user_id = %auth.user.user_id, "Getting subscription token");
                    let token = aggregate
                        .services
                        .read_model()
                        .subscription_token_generator
                        .generate(&auth.user.user_id, &labour_id.to_string());
                    ApiResult::from_json_result(Ok(serde_json::json!({ "token": token })))
                }
                SubscriptionQuery::GetSubscriptions { labour_id } => {
                    info!(labour_id = %labour_id, user_id = %auth.user.user_id, "Getting subscriptions");
                    let subscriptions = aggregate
                        .services
                        .read_model()
                        .subscription_query
                        .get(100, None) // TODO
                        .map(|items| build_paginated_response(items, 100));
                    ApiResult::from_json_result(subscriptions)
                }
            }
        }
    }
}

fn build_paginated_response<T: Cursor>(mut items: Vec<T>, limit: usize) -> PaginatedResponse<T> {
    let has_more = items.len() > limit;
    if has_more {
        items.pop();
    }

    let next_cursor = has_more.then(|| items.last()).flatten().map(|last_item| {
        let cursor_str = format!("{}|{}", last_item.updated_at().to_rfc3339(), last_item.id());
        BASE64_URL_SAFE_NO_PAD.encode(cursor_str)
    });

    PaginatedResponse {
        data: items,
        next_cursor,
        has_more,
    }
}
