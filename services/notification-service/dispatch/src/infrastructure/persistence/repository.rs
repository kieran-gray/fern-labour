use anyhow::{Context, Result, anyhow};
use async_trait::async_trait;
use worker::D1Database;

use crate::{
    domain::{
        repository::TrackedNotificationRepositoryTrait, tracked_notification::TrackedNotification,
    },
    infrastructure::persistence::models::TrackedNotificationRow,
};

pub struct D1TrackedNotificationRepository {
    db: D1Database,
}

impl D1TrackedNotificationRepository {
    pub fn create(db: D1Database) -> Self {
        Self { db }
    }
}

#[async_trait(?Send)]
impl TrackedNotificationRepositoryTrait for D1TrackedNotificationRepository {
    async fn get(&self, external_id: &str) -> Result<TrackedNotification> {
        let result: Option<TrackedNotificationRow> = self
            .db
            .prepare("SELECT * FROM notification_external_id_lookup WHERE external_id = ?1")
            .bind(&[external_id.to_string().into()])
            .context("Failed to prepare notification external id lookup")?
            .first(None)
            .await
            .context("Failed to lookup external id")?;

        match result {
            Some(row) => row.to_tracked_notification(),
            None => Err(anyhow!("Tracked Notification with external id not found")),
        }
    }

    async fn put(&self, tracked_notification: &TrackedNotification) -> Result<()> {
        let tracked_notification_row =
            TrackedNotificationRow::from_tracked_notification(tracked_notification)?;
        self.db
            .prepare(
                "INSERT INTO notification_external_id_lookup (
                    external_id, notification_id, channel, provider, created_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5)",
            )
            .bind(&[
                tracked_notification_row.external_id.into(),
                tracked_notification_row.notification_id.into(),
                tracked_notification_row.channel.into(),
                tracked_notification_row.provider.into(),
                tracked_notification_row.created_at.into(),
            ])
            .context("Failed to prepare tracked notification put")?
            .run()
            .await
            .context("Failed to put tracked notification")?;

        Ok(())
    }
}
