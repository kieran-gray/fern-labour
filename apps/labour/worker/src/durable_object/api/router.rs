use worker::{Method, Request, Response, Result};

use crate::durable_object::{
    api::{
        middleware::with_auth_context,
        routes::{
            admin::handle_admin_command,
            contractions::{handle_contraction_command, handle_contraction_query},
            events::handle_events_query,
            labour::{
                handle_labour_api_command, handle_labour_domain_command, handle_labour_query,
            },
            labour_updates::{handle_labour_update_command, handle_labour_update_query},
            subscriptions::{
                handle_subscriber_command, handle_subscription_command, handle_subscription_query,
            },
            user::handle_user_query,
        },
    },
    state::AggregateServices,
};

pub struct RequestContext<'a> {
    pub data: &'a AggregateServices,
}

impl<'a> RequestContext<'a> {
    pub fn new(data: &'a AggregateServices) -> Self {
        Self { data }
    }
}

pub async fn route_request(req: Request, services: &AggregateServices) -> Result<Response> {
    let method = req.method();
    let path = req.path();
    let ctx = RequestContext::new(services);

    match (method, path.as_str()) {
        (Method::Post, "/labour/domain") => {
            with_auth_context(handle_labour_domain_command, req, ctx).await
        }
        (Method::Post, "/labour/command") => {
            with_auth_context(handle_labour_api_command, req, ctx).await
        }
        (Method::Post, "/contraction/command") => {
            with_auth_context(handle_contraction_command, req, ctx).await
        }
        (Method::Post, "/labour-update/command") => {
            with_auth_context(handle_labour_update_command, req, ctx).await
        }
        (Method::Post, "/subscription/command") => {
            with_auth_context(handle_subscription_command, req, ctx).await
        }
        (Method::Post, "/subscriber/command") => {
            with_auth_context(handle_subscriber_command, req, ctx).await
        }
        (Method::Post, "/admin/command") => with_auth_context(handle_admin_command, req, ctx).await,
        (Method::Post, "/labour/query") => with_auth_context(handle_labour_query, req, ctx).await,
        (Method::Post, "/contraction/query") => {
            with_auth_context(handle_contraction_query, req, ctx).await
        }
        (Method::Post, "/labour-update/query") => {
            with_auth_context(handle_labour_update_query, req, ctx).await
        }
        (Method::Post, "/subscription/query") => {
            with_auth_context(handle_subscription_query, req, ctx).await
        }
        (Method::Post, "/user/query") => with_auth_context(handle_user_query, req, ctx).await,
        (Method::Get, "/labour/events") => with_auth_context(handle_events_query, req, ctx).await,
        _ => Response::error("Not Found", 404),
    }
}
