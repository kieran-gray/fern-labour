use fern_labour_labour_shared::ApiQuery;
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    http::{router::RequestContext, ApiResult},
    read_side::query_handler::QueryHandler,
};

pub async fn handle_query(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let query: ApiQuery = match req.json().await {
        Ok(q) => q,
        Err(e) => {
            error!(error = ?e, "Failed to parse ApiQuery");
            return Response::error("Failed to parse request body", 400);
        }
    };

    info!(query = ?query, user_id = %user.user_id, "Processing query");

    let handler = QueryHandler::new(ctx.data.read_model());
    let result = handler.handle(query, &user);

    if let Err(ref err) = result {
        error!(error = %err, "Query execution failed");
    } else {
        info!("Query executed successfully");
    }

    Ok(ApiResult::from_json_result(result).into_response())
}
