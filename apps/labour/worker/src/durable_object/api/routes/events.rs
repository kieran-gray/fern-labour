use fern_labour_workers_shared::User;
use tracing::{error, info};
use worker::{Request, Response};

use crate::durable_object::{api::ApiResult, api::router::RequestContext};

pub async fn handle_events_query(
    _req: Request,
    ctx: RequestContext<'_>,
    user: User,
) -> worker::Result<Response> {
    info!(auth_user_id = %user.user_id, "Processing events query");

    let result = ctx.data.read_model().event_query.get_event_stream();

    if let Err(ref err) = result {
        error!("Query execution failed: {}", err);
    } else {
        info!("Query executed successfully");
    }

    Ok(ApiResult::from_json_result(result).into_response())
}
