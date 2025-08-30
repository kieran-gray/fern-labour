use std::sync::Arc;

use crate::application::services::notification_service::NotificationServiceTrait;

use super::config::Config;

#[derive(Clone)]
pub struct AppState {
    pub config: Config,
    pub notification_service: Arc<dyn NotificationServiceTrait>,
}

impl AppState {
    pub fn new(config: Config, notification_service: Arc<dyn NotificationServiceTrait>) -> Self {
        Self {
            config,
            notification_service,
        }
    }
}
