use std::{collections::HashMap, str::FromStr, sync::Arc};

use async_trait::async_trait;
use uuid::Uuid;

use crate::{
    application::{
        dtos::notification::NotificationDTO,
        exceptions::AppError,
        services::{
            notification_generation_service::NotificationGenerationServiceTrait,
            notification_service::NotificationServiceTrait,
        },
    },
    domain::{
        entity::Notification,
        enums::{NotificationChannel, NotificationStatus, NotificationTemplate},
        exceptions::InvalidNotificationStatus,
        repository::NotificationRepository as NotificationRepositoryInterface,
    },
};

pub struct NotificationService {
    pub repo: Arc<dyn NotificationRepositoryInterface + Send + Sync>,
    pub notification_generation_service: Arc<dyn NotificationGenerationServiceTrait>,
}

impl NotificationService {
    pub fn create(
        notification_repo: Arc<dyn NotificationRepositoryInterface>,
        notification_generation_service: Arc<dyn NotificationGenerationServiceTrait>,
    ) -> Arc<dyn NotificationServiceTrait> {
        Arc::new(Self {
            repo: notification_repo,
            notification_generation_service,
        })
    }

    async fn _get_notification(
        &self,
        notification_id: &str,
    ) -> Result<Option<Notification>, AppError> {
        let notification_id = match Uuid::try_parse(&notification_id) {
            Ok(id) => id,
            Err(_) => return Err(AppError::InvalidNotificationId(notification_id.to_string())),
        };
        match self.repo.get_by_id(notification_id).await {
            Ok(notification) => Ok(notification),
            Err(err) => Err(AppError::DatabaseError(err)),
        }
    }

    async fn _get_notification_by_external_id(
        &self,
        external_id: &str,
    ) -> Result<Option<Notification>, AppError> {
        match self.repo.get_by_external_id(external_id).await {
            Ok(notification) => Ok(notification),
            Err(err) => Err(AppError::DatabaseError(err)),
        }
    }
}

#[async_trait]
impl NotificationServiceTrait for NotificationService {
    async fn create_notification(
        &self,
        channel: String,
        destination: String,
        template: String,
        data: HashMap<String, String>,
        metadata: Option<HashMap<String, String>>,
        status: Option<String>,
    ) -> Result<NotificationDTO, AppError> {
        let channel = NotificationChannel::from_str(&channel);
        if let Err(error) = channel {
            return Err(AppError::ValidationError(error.to_string()));
        }
        let channel = channel.unwrap();

        let notification_status: Result<Option<NotificationStatus>, InvalidNotificationStatus> =
            Ok(None);
        if status.is_some() {
            let notification_status = NotificationStatus::from_str(&status.unwrap());
            if let Err(error) = notification_status {
                return Err(AppError::ValidationError(error.to_string()));
            }
        }
        let notification_status = notification_status.unwrap();

        let notification_template = NotificationTemplate::from_str(&template);
        if let Err(error) = notification_template {
            return Err(AppError::ValidationError(error.to_string()));
        }
        let notification_template = notification_template.unwrap();

        let notification = Notification::create(
            channel,
            destination,
            notification_template,
            data,
            notification_status,
            metadata,
        );

        if let Err(err) = self.repo.save(&notification).await {
            tracing::error!("Error creating notification: {err}");
            return Err(AppError::DatabaseError(err));
        }

        Ok(NotificationDTO::from(notification))
    }

    async fn update_notification(
        &self,
        notification_id: String,
        status: String,
        external_id: Option<String>,
    ) -> Result<NotificationDTO, AppError> {
        let notification_status = NotificationStatus::from_str(&status);
        if let Err(error) = notification_status {
            return Err(AppError::ValidationError(error.to_string()));
        }
        let notification_status = notification_status.unwrap();

        let mut notification = match self._get_notification(&notification_id).await? {
            Some(notification) => notification,
            None => {
                return Err(AppError::NotFound(format!(
                    "Notification not found by id: {}",
                    notification_id
                )));
            }
        };

        if let Some(external_id) = external_id {
            notification.set_external_id(external_id);
        };
        notification.set_status(notification_status);

        if let Err(err) = self.repo.save(&notification).await {
            tracing::error!("Error saving notification: {err}");
            return Err(AppError::DatabaseError(err));
        }

        Ok(NotificationDTO::from(notification))
    }

    async fn status_callback(&self, external_id: String, status: String) -> Result<bool, AppError> {
        let notification_status = NotificationStatus::from_str(&status);
        if let Err(error) = notification_status {
            return Err(AppError::ValidationError(error.to_string()));
        }
        let notification_status = notification_status.unwrap();

        let mut notification = match self._get_notification_by_external_id(&external_id).await? {
            Some(notification) => notification,
            None => {
                return Err(AppError::NotFound(format!(
                    "Notification not found by external id: {}",
                    external_id
                )));
            }
        };

        notification.set_status(notification_status);

        if let Err(err) = self.repo.save(&notification).await {
            tracing::error!("Error saving notification: {err}");
            return Err(AppError::DatabaseError(err));
        }

        Ok(true)
    }
}
