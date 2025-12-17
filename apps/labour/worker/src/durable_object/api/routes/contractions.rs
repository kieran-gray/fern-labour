use chrono::DateTime;
use fern_labour_event_sourcing_rs::{CommandEnvelope, DecodedCursor, PaginatedResponse};
use fern_labour_labour_shared::{ContractionCommand, ContractionQuery};
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    api::router::RequestContext,
    api::{ApiResult, utils::build_paginated_response},
    read_side::read_models::contractions::ContractionReadModelQueryHandler,
    write_side::domain::LabourCommand,
};

pub async fn handle_contraction_command(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(envelope) = req.json::<CommandEnvelope<ContractionCommand>>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(
        aggregate_id = %envelope.metadata.aggregate_id,
        correlation_id = %envelope.metadata.correlation_id,
        user_id = %envelope.metadata.user_id,
        auth_user_id = %user.user_id,
        idempotency_key = %envelope.metadata.idempotency_key,
        "Processing contraction command"
    );

    let domain_command = LabourCommand::from(envelope.command);

    let result = ctx
        .data
        .write_model()
        .labour_command_processor
        .handle_command(domain_command, user);

    if let Err(ref err) = result {
        error!("Command execution failed: {}", err);
    } else {
        info!("Command executed successfully");
    }

    Ok(ApiResult::from_unit_result(result).into_response())
}

pub async fn handle_contraction_query(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(query) = req.json::<ContractionQuery>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(query = ?query, auth_user_id = %user.user_id, "Processing contraction query");

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
            ctx.data
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
            ctx.data
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

    Ok(ApiResult::from_json_result(result).into_response())
}
