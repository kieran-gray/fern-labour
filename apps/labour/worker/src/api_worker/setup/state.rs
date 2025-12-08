use anyhow::{Context, Result};
use fern_labour_workers_shared::{
    ConfigTrait,
    clients::{AuthServiceClient, DurableObjectCQRSClient, FetcherAuthServiceClient},
};
use worker::Env;

use crate::api_worker::Config;

pub struct AppState {
    pub config: Config,
    pub auth_service: Box<dyn AuthServiceClient>,
    pub do_client: DurableObjectCQRSClient,
}

impl AppState {
    fn create_do_client(env: &Env) -> Result<DurableObjectCQRSClient> {
        let aggregate_namespace = env
            .durable_object("LABOUR_AGGREGATE")
            .context("Missing binding LABOUR_AGGREGATE")?;

        Ok(DurableObjectCQRSClient::create(aggregate_namespace))
    }

    fn create_auth_service(env: &Env) -> Result<Box<dyn AuthServiceClient>> {
        let auth_service_fetcher = env
            .service("AUTH_SERVICE_API")
            .context("Missing binding AUTH_SERVICE_API")?;

        Ok(Box::new(FetcherAuthServiceClient::create(
            auth_service_fetcher,
        )))
    }

    pub fn from_env(env: &Env) -> Result<Self> {
        let config = Config::from_env(env)?;
        let auth_service = Self::create_auth_service(env)?;

        let do_client = Self::create_do_client(env)?;

        Ok(Self {
            config,
            auth_service,
            do_client,
        })
    }
}
