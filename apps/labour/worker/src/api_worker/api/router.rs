use worker::Router;

use crate::api_worker::AppState;
use crate::api_worker::api::middleware::authenticated;
use crate::api_worker::api::middleware::create_options_handler;
use crate::api_worker::api::routes::commands::handle_command;
use crate::api_worker::api::routes::labour::handle_plan_labour;

pub fn create_router(app_state: AppState) -> Router<'static, AppState> {
    Router::with_data(app_state)
        .post_async("/api/v1/labour/plan", |req, ctx| {
            authenticated(handle_plan_labour, req, ctx)
        })
        .options("/api/v1/labour/plan", create_options_handler)
        .post_async("/api/v1/command", |req, ctx| {
            authenticated(handle_command, req, ctx)
        })
        .options("/api/v1/command", create_options_handler)
}
