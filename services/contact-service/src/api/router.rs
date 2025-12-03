use worker::*;

use crate::api::routes::contact_queries::get_contact_message_activity_handler;
use crate::api::routes::{
    contact_commands::create_contact_message_handler, contact_queries::get_contact_messages_handler,
};
use crate::api::utils::handlers::create_options_handler;
use crate::api::utils::routes::{authenticated, public};
use crate::setup::app_state::AppState;

pub fn create_router(app_state: AppState) -> Router<'static, AppState> {
    let router = Router::with_data(app_state);
    router
        .post_async("/api/v1/contact-us/", |req, ctx| {
            public(create_contact_message_handler, req, ctx)
        })
        .get_async("/api/v1/contact-messages/", |req, ctx| {
            authenticated(get_contact_messages_handler, req, ctx)
        })
        .get_async("/api/v1/contact-messages/activity/:days", |req, ctx| {
            authenticated(get_contact_message_activity_handler, req, ctx)
        })
        .options("/api/v1/contact-us/", create_options_handler)
        .options("/api/v1/contact-messages/", create_options_handler)
}
