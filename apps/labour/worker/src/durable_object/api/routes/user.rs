use fern_labour_labour_shared::{ApiQuery, queries::user::UserQuery};
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{
    api::ApiResult, api::router::RequestContext, read_side::query_handler::QueryHandler,
};

pub async fn handle_user_query(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(query) = req.json::<UserQuery>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(query = ?query, auth_user_id = %user.user_id, "Processing user query");

    let handler = QueryHandler::new(ctx.data.read_model());
    let result = handler.handle(ApiQuery::User(query), &user);

    if let Err(ref err) = result {
        error!("Query execution failed: {}", err);
    } else {
        info!("Query executed successfully");
    }

    Ok(ApiResult::from_json_result(result).into_response())
}
