use std::str::FromStr;

use serde::de::DeserializeOwned;
use worker::Env;

use crate::setup::exceptions::SetupError;

pub trait ConfigTrait<C: Sized> {
    fn from_env(env: &Env) -> Result<C, SetupError>;

    fn parse<T: FromStr>(env: &Env, var: &str) -> Result<T, SetupError> {
        let type_name = std::any::type_name::<T>();
        let env_var: T = env
            .var(var)
            .map_err(|e| SetupError::MissingVariable(e.to_string()))?
            .to_string()
            .parse()
            .map_err(|_| SetupError::InvalidVariable(format!("{var} should be {type_name}")))?;
        Ok(env_var)
    }

    fn parse_csv(env: &Env, var: &str) -> Result<Vec<String>, SetupError> {
        let env_var = env
            .var(var)
            .map_err(|_| SetupError::MissingVariable(var.to_string()))?
            .to_string()
            .split(',')
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect();
        Ok(env_var)
    }

    fn parse_json<T: DeserializeOwned>(env: &Env, var: &str) -> Result<T, SetupError> {
        let env_var: T = env
            .object_var::<T>(var)
            .map_err(|e| SetupError::MissingVariable(e.to_string()))?;
        Ok(env_var)
    }
}
