use worker::*;

use crate::api::routes::render::{render, render_async};
use crate::api::utils::routes::with_service_id;
use crate::setup::app_state::AppState;

pub fn create_router(app_state: AppState) -> Router<'static, AppState> {
    Router::with_data(app_state)
        .post_async("/api/v1/render-async", |req, ctx| {
            with_service_id(render_async, req, ctx)
        })
        .post_async("/api/v1/render", |req, ctx| {
            with_service_id(render, req, ctx)
        })
}
