use std::sync::Arc;

use tracing::error;
use worker::Env;

use crate::{
    application::services::{
        alert_service::LogAlertService,
        contact_message::{ContactMessageService, ContactMessageServiceTrait},
        contact_message_queries::{ContactMessageQueryService, ContactMessageQueryServiceTrait},
    },
    infrastructure::{
        persistence::contact_message_repository::ContactMessageRepository,
        services::{
            request_validation_service::CloudflareRequestValidationService,
            slack_alert_service::SlackAlertService,
        },
    },
    setup::config::Config,
};

use fern_labour_workers_shared::clients::{AuthServiceClient, FetcherAuthServiceClient};
use fern_labour_workers_shared::{SetupError, clients::WorkerHttpClient};

pub struct AppState {
    pub config: Config,
    pub contact_message_service: Arc<dyn ContactMessageServiceTrait>,
    pub contact_message_query_service: Arc<dyn ContactMessageQueryServiceTrait>,
    pub auth_service: Arc<dyn AuthServiceClient>,
}

impl AppState {
    pub fn from_env(env: &Env, config: Config) -> Result<Self, SetupError> {
        let db = env.d1("DB").map_err(|e| {
            error!("Failed to get D1 binding: {:?}", e);
            SetupError::MissingBinding("DB".to_string())
        })?;

        let auth_service_fetcher = env.service("AUTH").map_err(|e| {
            error!("Failed to get Auth Service binding: {:?}", e);
            SetupError::MissingBinding("AUTH".to_string())
        })?;

        let auth_service = Arc::new(FetcherAuthServiceClient::create(auth_service_fetcher));

        let http_client = Arc::new(WorkerHttpClient::new());

        let alert_service = match config.slack {
            Some(ref slack_config) => SlackAlertService::create(
                &slack_config.token,
                &slack_config.channel,
                &slack_config.url,
                http_client.clone(),
            ),
            None => LogAlertService::create(),
        };

        let request_validation_service = CloudflareRequestValidationService::create(
            &config.siteverify_url,
            &config.secret_key,
            http_client,
        );

        let contact_message_repository = ContactMessageRepository::create(db);
        let contact_message_service = ContactMessageService::create(
            contact_message_repository.clone(),
            request_validation_service,
            alert_service,
        );
        let contact_message_query_service =
            ContactMessageQueryService::create(contact_message_repository.clone());

        Ok(Self {
            config,
            contact_message_service,
            contact_message_query_service,
            auth_service,
        })
    }
}
