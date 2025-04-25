use std::collections::HashMap;

use crate::domain::{
    entity::Notification, repository::NotificationRepository as NotificationRepositoryInterface,
};
use crate::infrastructure::models::NotificationModel;
use async_trait::async_trait;
use sqlx::{Pool, Postgres};
use uuid::Uuid;

#[derive(Debug, Clone)]
pub struct NotificationRepository {
    pool: Pool<Postgres>,
}

impl NotificationRepository {
    pub fn create(pool: Pool<Postgres>) -> Self {
        Self { pool }
    }

    fn serialize_data(data: &HashMap<String, String>) -> Result<serde_json::Value, sqlx::Error> {
        serde_json::to_value(data).map_err(|e| sqlx::Error::Encode(Box::new(e)))
    }

    fn serialize_metadata(
        metadata: &Option<HashMap<String, String>>,
    ) -> Result<serde_json::Value, sqlx::Error> {
        match metadata {
            Some(m) => serde_json::to_value(m).map_err(|e| sqlx::Error::Encode(Box::new(e))),
            None => Ok(serde_json::Value::Null),
        }
    }
}

#[async_trait]
impl NotificationRepositoryInterface for NotificationRepository {
    async fn get_by_id(&self, id: Uuid) -> Result<Option<Notification>, sqlx::Error> {
        let row = sqlx::query!(
            r#"SELECT 
                id,
                status,
                notification_type,
                destination,
                template,
                data as "data: serde_json::Value",
                metadata as "metadata: serde_json::Value",
                external_id
            FROM notifications
            WHERE id = $1"#,
            id
        )
        .fetch_optional(&self.pool)
        .await?;

        match row {
            Some(row) => {
                let data: HashMap<String, String> = serde_json::from_value(row.data)
                    .map_err(|e| sqlx::Error::Decode(Box::new(e)))?;

                let metadata: Option<HashMap<String, String>> = match row.metadata {
                    None => None,
                    Some(metadata) => Some(
                        serde_json::from_value(metadata)
                            .map_err(|e| sqlx::Error::Decode(Box::new(e)))?,
                    ),
                };

                let model = NotificationModel::create(
                    row.id,
                    row.status,
                    row.notification_type,
                    row.destination,
                    row.template,
                    sqlx::types::Json(data),
                    sqlx::types::Json(metadata),
                    row.external_id,
                );

                match Notification::try_from(model) {
                    Ok(notification) => Ok(Some(notification)),
                    Err(conv_err) => Err(sqlx::Error::Decode(Box::new(conv_err))),
                }
            }
            None => Ok(None),
        }
    }

    async fn get_by_external_id(
        &self,
        external_id: String,
    ) -> Result<Option<Notification>, sqlx::Error> {
        let row = sqlx::query!(
            r#"SELECT
                id,
                status,
                notification_type,
                destination,
                template,
                data,
                metadata,
                external_id
            FROM notifications
            WHERE external_id = $1"#,
            external_id
        )
        .fetch_optional(&self.pool)
        .await?;

        match row {
            Some(row) => {
                let data: HashMap<String, String> = serde_json::from_value(row.data)
                    .map_err(|e| sqlx::Error::Decode(Box::new(e)))?;

                let metadata: Option<HashMap<String, String>> = match row.metadata {
                    None => None,
                    Some(metadata) => Some(
                        serde_json::from_value(metadata)
                            .map_err(|e| sqlx::Error::Decode(Box::new(e)))?,
                    ),
                };

                let model = NotificationModel::create(
                    row.id,
                    row.status,
                    row.notification_type,
                    row.destination,
                    row.template,
                    sqlx::types::Json(data),
                    sqlx::types::Json(metadata),
                    row.external_id,
                );

                match Notification::try_from(model) {
                    Ok(notification) => Ok(Some(notification)),
                    Err(conv_err) => Err(sqlx::Error::Decode(Box::new(conv_err))),
                }
            }
            None => Ok(None),
        }
    }

    async fn save(&self, notification: &Notification) -> Result<bool, sqlx::Error> {
        let data_json = Self::serialize_data(&notification.data)?;
        let metadata_json = Self::serialize_metadata(&notification.metadata)?;

        let res = sqlx::query!(
            r#"
            INSERT INTO notifications (
                id, status, notification_type, destination, template, data, metadata, external_id
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8
            )
            ON CONFLICT (id) DO UPDATE SET
                status = EXCLUDED.status,
                notification_type = EXCLUDED.notification_type,
                destination = EXCLUDED.destination,
                template = EXCLUDED.template,
                data = EXCLUDED.data,
                metadata = EXCLUDED.metadata,
                external_id = EXCLUDED.external_id
            "#,
            notification.id,
            notification.status.to_string(),
            notification.notification_type.to_string(),
            notification.destination,
            notification.template.to_string(),
            data_json,
            metadata_json,
            notification.external_id
        )
        .execute(&self.pool)
        .await?;
        return Ok(res.rows_affected() > 0);
    }

    async fn delete(&self, notification: &Notification) -> Result<bool, sqlx::Error> {
        let res = sqlx::query!(
            r#"DELETE FROM notifications WHERE id = $1"#,
            notification.id
        )
        .execute(&self.pool)
        .await?;

        Ok(res.rows_affected() > 0)
    }
}
