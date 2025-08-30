use sqlx::PgPool;

use crate::infrastructure::services::notification_generation_service::NotificationGenerationService;
use crate::infrastructure::template_engines::email_template_engine::EmailTemplateEngine;
use crate::infrastructure::template_engines::sms_template_engine::SMSTemplateEngine;
use crate::infrastructure::{
    notification_repository::NotificationRepository,
    services::notification_service::NotificationService,
};
use crate::setup::app_state::AppState;
use crate::setup::config::Config;

use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

/// Constructs and wires all application services and returns a configured AppState.
pub fn build_app_state(pool: PgPool, config: Config) -> AppState {
    let notification_repository = NotificationRepository::create(pool.clone());
    let email_template_engine = EmailTemplateEngine::create();
    let sms_template_engine = SMSTemplateEngine::create();

    let notification_generation_service = NotificationGenerationService::create(
        notification_repository.clone(),
        email_template_engine,
        sms_template_engine,
    );
    let notification_service = NotificationService::create(
        notification_repository.clone(),
        notification_generation_service.clone(),
    );

    AppState::new(config, notification_service)
}

/// Setup tracing for the application.
/// This function initializes the tracing subscriber with a default filter and formatting.
pub fn setup_tracing() {
    dotenv::dotenv().ok();

    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,sqlx=info,tower_http=info,axum::rejection=trace".into()),
        )
        .with(
            tracing_subscriber::fmt::layer()
                .with_file(true)
                .with_line_number(true)
                .with_thread_ids(true)
                .with_thread_names(true)
                .with_target(true)
                .with_span_events(tracing_subscriber::fmt::format::FmtSpan::CLOSE),
        )
        .init();
}

/// Shutdown signal handler
/// This function listens for a shutdown signal (CTRL+C) and logs a message when received.
pub async fn shutdown_signal() {
    tokio::signal::ctrl_c()
        .await
        .expect("Failed to install CTRL+C signal handler");
}
