use serde::Deserialize;
use sqlx::{
    PgPool,
    postgres::{PgConnectOptions, PgPoolOptions},
};
use std::{env, str::FromStr};

/// Config is a struct that holds the configuration for the application.
#[derive(Default, Clone, Debug, Deserialize)]
pub struct Config {
    pub environment: String,

    pub database_url: String,

    pub database_max_connections: u32,
    pub database_min_connections: u32,

    pub service_host: String,
    pub service_port: String,

    pub smtp_host: Option<String>,
    pub smtp_user: Option<String>,
    pub smtp_password: Option<String>,
    pub emails_from_email: Option<String>,
    pub emails_from_name: Option<String>,
    pub smtp_tls: bool,
    pub smtp_ssl: bool,
    pub smtp_port: u32,
    pub support_email: String,
    pub tracking_link: String,

    pub account_sid: Option<String>,
    pub auth_token: Option<String>,
    pub sms_from_number: Option<String>,
    pub messaging_service_sid: Option<String>,

    pub project_id: String,
    pub retries: u32,
}

/// from_env reads the environment variables and returns a Config struct.
/// It uses the dotenv crate to load environment variables from a .env file if it exists.
/// It returns a Result with the Config struct or an error if any of the environment variables are missing.
impl Config {
    pub fn from_env() -> Result<Self, env::VarError> {
        dotenv::dotenv().ok();

        Ok(Self {
            environment: env::var("ENVIRONMENT")?,

            database_url: env::var("DATABASE_URL")?,

            database_max_connections: env::var("DATABASE_MAX_CONNECTIONS")
                .map(|s| s.parse::<u32>().unwrap_or(5))
                .unwrap_or(5),
            database_min_connections: env::var("DATABASE_MIN_CONNECTIONS")
                .map(|s| s.parse::<u32>().unwrap_or(1))
                .unwrap_or(1),

            service_host: env::var("SERVICE_HOST")?,
            service_port: env::var("SERVICE_PORT")?,

            smtp_host: env::var("SMTP_HOST").map(|s| Some(s)).unwrap_or(None),
            smtp_user: env::var("SMTP_USER").map(|s| Some(s)).unwrap_or(None),
            smtp_password: env::var("SMTP_PASSWORD").map(|s| Some(s)).unwrap_or(None),
            smtp_tls: env::var("SMTP_TLS")
                .map(|s| bool::from_str(&s).unwrap_or(true))
                .unwrap_or(true),
            smtp_ssl: env::var("SMTP_SSL")
                .map(|s| bool::from_str(&s).unwrap_or(false))
                .unwrap_or(false),
            smtp_port: env::var("SMTP_PORT")
                .map(|s| s.parse::<u32>().unwrap_or(587))
                .unwrap_or(587),

            emails_from_email: env::var("EMAILS_FROM_EMAIL")
                .map(|s| Some(s))
                .unwrap_or(None),
            emails_from_name: env::var("EMAILS_FROM_NAME")
                .map(|s| Some(s))
                .unwrap_or(None),
            support_email: env::var("SUPPORT_EMAIL")
                .unwrap_or(String::from("support@fernlabour.com")),
            tracking_link: env::var("TRACKING_LINK")
                .unwrap_or(String::from("https://track.fernlabour.com")),

            account_sid: env::var("TWILIO_ACCOUNT_SID")
                .map(|s| Some(s))
                .unwrap_or(None),
            auth_token: env::var("TWILIO_AUTH_TOKEN")
                .map(|s| Some(s))
                .unwrap_or(None),
            sms_from_number: env::var("SMS_FROM_NUMBER").map(|s| Some(s)).unwrap_or(None),
            messaging_service_sid: env::var("MESSAGING_SERVICE_SID")
                .map(|s| Some(s))
                .unwrap_or(None),

            project_id: env::var("GCP_PROJECT_ID")?,
            retries: env::var("GCP_PRODUCER_RETRIES")
                .map(|s| s.parse::<u32>().unwrap_or(3))
                .unwrap_or(3),
        })
    }
}

pub async fn setup_database(config: &Config) -> Result<PgPool, sqlx::Error> {
    // Create connection options
    let connect_options = PgConnectOptions::from_str(&config.database_url)
        .map_err(|e| {
            tracing::error!("Failed to parse database URL: {}", e);
            e
        })?
        .clone();

    let pool = PgPoolOptions::new()
        .max_connections(config.database_max_connections)
        .min_connections(config.database_min_connections)
        .connect_with(connect_options)
        .await?;

    Ok(pool)
}
