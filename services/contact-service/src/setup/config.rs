use fern_labour_shared::{ConfigTrait, SetupError};
use worker::Env;

#[derive(Clone)]
pub struct Config {
    pub siteverify_url: String,
    pub secret_key: String,
    pub allowed_origins: Vec<String>,
    pub slack: Option<SlackConfig>,
}

#[derive(Clone)]
pub struct SlackConfig {
    pub token: String,
    pub channel: String,
    pub url: String,
}

impl ConfigTrait<Config> for Config {
    fn from_env(env: &Env) -> Result<Self, SetupError> {
        let siteverify_url = Config::parse(env, "CLOUDFLARE_SITEVERIFY_URL")?;
        let secret_key = Config::parse(env, "CLOUDFLARE_SECRET_KEY")?;
        let allowed_origins = Config::parse_csv(env, "ALLOWED_ORIGINS")?;

        let slack = match (
            Config::parse(env, "SLACK_TOKEN"),
            Config::parse(env, "SLACK_CHANNEL"),
            Config::parse(env, "SLACK_MESSAGE_URL"),
        ) {
            (Ok(token), Ok(channel), Ok(url)) => Some(SlackConfig {
                token,
                channel,
                url,
            }),
            _ => None,
        };

        Ok(Config {
            siteverify_url,
            secret_key,
            allowed_origins,
            slack,
        })
    }
}
