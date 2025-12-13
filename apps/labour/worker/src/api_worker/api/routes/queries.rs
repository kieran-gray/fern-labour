use fern_labour_labour_shared::ApiQuery;
use fern_labour_workers_shared::CorsContext;
use tracing::error;
use worker::{Request, Response, RouteContext};

use crate::api_worker::{AppState, api::exceptions::ApiError};

pub async fn handle_query(
    mut req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user_id: String,
) -> worker::Result<Response> {
    let query: ApiQuery = match req.json().await {
        Ok(query) => query,
        Err(e) => {
            error!(user_id = %user_id, error = ?e, "Failed to parse request body");
            let response = Response::from(ApiError::ValidationError(
                "Failed to parse request body".into(),
            ));
            return Ok(cors_context.add_to_response(response));
        }
    };

    let labour_id = query.labour_id();

    let response = match query {
        ApiQuery::Labour(qry) => ctx
            .data
            .do_client
            .query_with_body(labour_id, qry, user_id, "/labour/query")
            .await
            .map_err(|e| format!("Failed to send query to labour aggregate: {e}"))?,
        ApiQuery::Contraction(qry) => ctx
            .data
            .do_client
            .query_with_body(labour_id, qry, user_id, "/contraction/query")
            .await
            .map_err(|e| format!("Failed to send query to labour aggregate: {e}"))?,
        ApiQuery::LabourUpdate(qry) => ctx
            .data
            .do_client
            .query_with_body(labour_id, qry, user_id, "/labour-update/query")
            .await
            .map_err(|e| format!("Failed to send query to labour aggregate: {e}"))?,
    };

    Ok(cors_context.add_to_response(response))
}
