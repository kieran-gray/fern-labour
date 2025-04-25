use rust_notification_service::{
    api::router::create_router,
    setup::{
        bootstrap::{build_app_state, shutdown_signal},
        config::{Config, setup_database},
    },
};
use tracing::info;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = Config::from_env()?;
    let pool = setup_database(&config).await?;
    let state = build_app_state(pool, config.clone());
    let app = create_router(state);

    let addr = format!("{}:{}", config.service_host, config.service_port);

    info!("Server running at {addr}");

    let listener = tokio::net::TcpListener::bind(&addr).await?;

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    info!("Server shutdown complete");

    Ok(())
}
