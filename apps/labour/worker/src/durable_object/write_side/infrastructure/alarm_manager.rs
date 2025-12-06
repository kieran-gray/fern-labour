use anyhow::{Context, Result};
use worker::Storage;

pub struct AlarmManager {
    storage: Storage,
}

impl AlarmManager {
    pub fn create(storage: Storage) -> Self {
        Self { storage }
    }

    pub async fn set_alarm(&self, delay: i64) -> Result<()> {
        self.storage
            .set_alarm(delay)
            .await
            .context("Failed to set alarm")?;
        Ok(())
    }
}
