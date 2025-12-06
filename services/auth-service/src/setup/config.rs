use std::collections::HashMap;

use fern_labour_workers_shared::{ConfigTrait, SetupError};
use serde::Deserialize;
use worker::Env;

use crate::domain::{Issuer, IssuerRegistry};

#[derive(Clone)]
pub struct Config {
    pub issuers: IssuerRegistry,
    pub allowed_origins: Vec<String>,
    pub jwks_cache_ttl: u64,
}

#[derive(Clone, Deserialize, Debug)]
pub struct IssuerConfigDto {
    pub issuer_url: String,
    pub jwks_path: String,
    pub audience: Option<String>,
    pub name: String,
}

impl Config {
    fn build_issuer_registry(
        dtos: HashMap<String, IssuerConfigDto>,
    ) -> Result<IssuerRegistry, SetupError> {
        let mut issuers = HashMap::new();

        for (key, dto) in dtos {
            let issuer = Issuer::new(
                dto.name.clone(),
                dto.issuer_url,
                dto.jwks_path,
                dto.audience,
            )
            .map_err(|e| SetupError::InvalidVariable(format!("Invalid issuer '{}': {}", key, e)))?;

            issuers.insert(key, issuer);
        }

        Ok(IssuerRegistry::new(issuers))
    }
}

impl ConfigTrait<Config> for Config {
    fn from_env(env: &Env) -> Result<Self, SetupError> {
        let allowed_origins = Config::parse_csv(env, "ALLOWED_ORIGINS")?;
        let jwks_cache_ttl: u64 = Config::parse(env, "JWKS_CACHE_TTL").unwrap_or(43200);
        let issuers_map: HashMap<String, IssuerConfigDto> =
            Config::parse_json(env, "AUTH_ISSUERS")?;

        let issuers = Self::build_issuer_registry(issuers_map)?;

        Ok(Config {
            issuers,
            allowed_origins,
            jwks_cache_ttl,
        })
    }
}
