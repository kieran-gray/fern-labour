use fern_labour_labour_shared::ApiQuery;
use fern_labour_workers_shared::{CorsContext, clients::worker_clients::auth::User};
use tracing::error;
use worker::{Request, Response, RouteContext};

use crate::api_worker::{AppState, api::exceptions::ApiError};

pub async fn handle_query(
    mut req: Request,
    ctx: RouteContext<AppState>,
    cors_context: CorsContext,
    user: User,
) -> worker::Result<Response> {
    let query: ApiQuery = match req.json().await {
        Ok(query) => query,
        Err(e) => {
            error!(user_id = %user.user_id, error = ?e, "Failed to parse request body");
            let response = Response::from(ApiError::ValidationError(
                "Failed to parse request body".into(),
            ));
            return Ok(cors_context.add_to_response(response));
        }
    };

    let labour_id = query.labour_id();

    let (url, query_payload) = match query {
        ApiQuery::Labour(qry) => ("/labour/query", serde_json::to_value(qry)?),
        ApiQuery::Contraction(qry) => ("/contraction/query", serde_json::to_value(qry)?),
        ApiQuery::LabourUpdate(qry) => ("/labour-update/query", serde_json::to_value(qry)?),
        ApiQuery::Subscription(qry) => ("/subscription/query", serde_json::to_value(qry)?),
    };

    let mut do_response = ctx
        .data
        .do_client
        .query_with_body(labour_id, query_payload, &user, url)
        .await
        .map_err(|e| format!("Failed to send query to labour_aggregate: {e}"))?;

    let body = do_response.text().await?;
    let status = do_response.status_code();

    let mut new_response = Response::ok(body)?.with_status(status);
    let _ = new_response
        .headers_mut()
        .set("Content-Type", "application/json");

    Ok(cors_context.add_to_response(new_response))
}
