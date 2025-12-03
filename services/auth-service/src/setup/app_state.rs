use std::{collections::HashMap, sync::Arc};
use tracing::error;
use worker::Env;

use crate::{
    application::services::{
        authentication_service::{AuthenticationService, AuthenticationServiceTrait},
        identity_extraction_service::{ClaimsExtractor, IdentityExtractionService},
        token_validation_service::TokenValidationService,
    },
    infrastructure::{
        claims_extractors::{auth0::Auth0ClaimsExtractor, cloudflare::CloudflareClaimsExtractor},
        jwt_parser::JwtParser,
        repositories::jwks_repository::JwksRepository,
        signature_verifiers::rs256_verifier::RS256SignatureVerifier,
    },
    setup::config::Config,
};

use fern_labour_shared::{cache::KVCache, SetupError};

pub struct AppState {
    pub config: Config,
    pub auth_service: Arc<dyn AuthenticationServiceTrait>,
}

impl AppState {
    pub fn from_env(env: &Env, config: Config) -> Result<Self, SetupError> {
        let jwks_cache = env.kv("AUTH_JWKS_CACHE").map_err(|e| {
            error!("Failed to get KV binding: {:?}", e);
            SetupError::MissingBinding("AUTH_JWKS_CACHE".to_string())
        })?;

        let jwks_cache = KVCache::create(jwks_cache, config.jwks_cache_ttl);
        let jwks_repository = Arc::new(JwksRepository::create(jwks_cache));
        let signature_verifier = Arc::new(RS256SignatureVerifier);
        let jwt_parser = Arc::new(JwtParser);
        let token_validator = Arc::new(TokenValidationService::create(
            jwks_repository,
            config.issuers.clone(),
            signature_verifier,
            jwt_parser,
        ));

        let mut extractors: HashMap<String, Box<dyn ClaimsExtractor>> = HashMap::new();
        extractors.insert("auth0".to_string(), Box::new(Auth0ClaimsExtractor));
        extractors.insert(
            "cloudflare".to_string(),
            Box::new(CloudflareClaimsExtractor),
        );

        let identity_extractor = Arc::new(IdentityExtractionService::create(extractors));
        let auth_service = AuthenticationService::create(token_validator, identity_extractor);

        Ok(Self {
            config,
            auth_service: Arc::new(auth_service),
        })
    }
}
