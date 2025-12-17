use fern_labour_labour_shared::queries::user::UserQuery;
use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{api::ApiResult, api::router::RequestContext};

pub async fn handle_user_query(
    mut req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    let Ok(query) = req.json::<UserQuery>().await else {
        return Response::error("Failed to parse request body", 400);
    };

    info!(query = ?query, auth_user_id = %user.user_id, "Processing user query");

    let result = match query {
        UserQuery::GetUser { labour_id, user_id } => {
            info!(labour_id = %labour_id, user_id = %user_id, "Getting user");
            ctx.data.read_model().user_query.get_user_by_id(user_id)
        }
        UserQuery::GetUsers { labour_id } => {
            info!(labour_id = %labour_id, "Getting users");
            ctx.data.read_model().user_query.get_users()
        }
    };

    if let Err(ref err) = result {
        error!("Query execution failed: {}", err);
    } else {
        info!("Query executed successfully");
    }

    Ok(ApiResult::from_json_result(result).into_response())
}
