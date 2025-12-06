use fern_labour_workers_shared::{ConfigTrait, SetupError};
use worker::Env;

#[derive(Clone)]
pub struct Config {
    pub allowed_origins: Vec<String>,
    pub auth_enabled: bool,
}

impl ConfigTrait<Config> for Config {
    fn from_env(env: &Env) -> Result<Self, SetupError> {
        let allowed_origins = Config::parse_csv(env, "ALLOWED_ORIGINS")?;
        let auth_enabled: bool = Config::parse(env, "AUTH_ENABLED")?;

        Ok(Self {
            allowed_origins,
            auth_enabled,
        })
    }
}
