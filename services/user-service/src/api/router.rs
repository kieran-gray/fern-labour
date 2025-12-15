use worker::*;

use crate::api::routes::{
    commands::{create_user_handler, delete_user_handler, update_user_handler},
    queries::{get_current_user, get_user_by_id},
};
use crate::api::utils::handlers::create_options_handler;
use crate::api::utils::routes::authenticated;
use crate::setup::app_state::AppState;

pub fn create_router(app_state: AppState) -> Router<'static, AppState> {
    let router = Router::with_data(app_state);
    router
        // User commands
        .post_async("/api/v1/users", |req, ctx| {
            authenticated(create_user_handler, req, ctx)
        })
        .put_async("/api/v1/users/me", |req, ctx| {
            authenticated(update_user_handler, req, ctx)
        })
        .delete_async("/api/v1/users/me", |req, ctx| {
            authenticated(delete_user_handler, req, ctx)
        })
        // User queries
        .get_async("/api/v1/users/me", |req, ctx| {
            authenticated(get_current_user, req, ctx)
        })
        .get_async("/api/v1/users/:user_id", |req, ctx| {
            authenticated(get_user_by_id, req, ctx)
        })
        // OPTIONS for CORS
        .options("/api/v1/users", create_options_handler)
        .options("/api/v1/users/me", create_options_handler)
        .options("/api/v1/users/:user_id", create_options_handler)
}
