use std::sync::Arc;

use async_trait::async_trait;
use tracing::info;

use crate::application::exceptions::AppError;

#[async_trait(?Send)]
pub trait AlertServiceTrait: Send + Sync {
    async fn send_alert(&self, message: String) -> Result<(), AppError> {
        info!("New alert: {message}");
        Ok(())
    }
}

pub struct LogAlertService;

impl LogAlertService {
    pub fn create() -> Arc<dyn AlertServiceTrait> {
        Arc::new(Self)
    }
}

impl AlertServiceTrait for LogAlertService {}
