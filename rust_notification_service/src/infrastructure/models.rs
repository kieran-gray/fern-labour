use crate::domain::{
    entity::Notification,
    enums::{NotificationChannel, NotificationStatus, NotificationTemplate},
};
use sqlx::{FromRow, types::Json};
use std::{collections::HashMap, str::FromStr};
use uuid::Uuid;

use super::exceptions::InfrastructureError;

#[derive(FromRow, Debug)]
pub struct NotificationModel {
    id: Uuid,
    status: String,
    channel: String,
    destination: String,
    template: String,
    data: Json<HashMap<String, String>>,
    metadata: Json<Option<HashMap<String, String>>>,
    external_id: Option<String>,
}

impl NotificationModel {
    pub fn create(
        id: Uuid,
        status: String,
        channel: String,
        destination: String,
        template: String,
        data: Json<HashMap<String, String>>,
        metadata: Json<Option<HashMap<String, String>>>,
        external_id: Option<String>,
    ) -> Self {
        return Self {
            id,
            status,
            channel,
            destination,
            template,
            data,
            metadata,
            external_id,
        };
    }
}

impl TryFrom<NotificationModel> for Notification {
    type Error = InfrastructureError;

    fn try_from(row: NotificationModel) -> Result<Self, Self::Error> {
        Ok(Notification {
            id: row.id,
            status: NotificationStatus::from_str(&row.status).map_err(|e| {
                InfrastructureError::DatabaseRowToDomainConversionError(format!(
                    "Failed to parse status '{}': {}",
                    row.status, e
                ))
            })?,
            channel: NotificationChannel::from_str(&row.channel).map_err(|e| {
                InfrastructureError::DatabaseRowToDomainConversionError(format!(
                    "Failed to parse type '{}': {}",
                    row.channel, e
                ))
            })?,
            destination: row.destination,
            template: NotificationTemplate::from_str(&row.template).map_err(|e| {
                InfrastructureError::DatabaseRowToDomainConversionError(format!(
                    "Failed to parse template '{}': {}",
                    row.template, e
                ))
            })?,
            data: row.data.0,
            metadata: row.metadata.0,
            external_id: row.external_id,
        })
    }
}
