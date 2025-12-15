use std::sync::Arc;

use tracing::error;
use worker::Env;

use crate::{
    application::services::{
        user_commands::{UserCommandService, UserCommandServiceTrait},
        user_queries::{UserQueryService, UserQueryServiceTrait},
    },
    infrastructure::persistence::user_repository::UserRepository,
    setup::config::Config,
};

use fern_labour_workers_shared::SetupError;
use fern_labour_workers_shared::clients::{AuthServiceClient, FetcherAuthServiceClient};

pub struct AppState {
    pub config: Config,
    pub user_command_service: Arc<dyn UserCommandServiceTrait>,
    pub user_query_service: Arc<dyn UserQueryServiceTrait>,
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

        let user_repository = UserRepository::create(db);
        let user_command_service = UserCommandService::create(user_repository.clone());
        let user_query_service = UserQueryService::create(user_repository.clone());

        Ok(Self {
            config,
            user_command_service,
            user_query_service,
            auth_service,
        })
    }
}
