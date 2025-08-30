use std::{collections::HashMap, sync::Arc};

use async_trait::async_trait;
use uuid::Uuid;

use crate::{
    application::{
        dtos::notification_content::NotificationContentDTO,
        exceptions::AppError,
        services::{
            notification_generation_service::NotificationGenerationServiceTrait,
            template_engine::NotificationTemplateEngineTrait,
        },
    },
    domain::{
        entity::Notification,
        enums::{NotificationChannel, NotificationTemplate},
        repository::NotificationRepository as NotificationRepositoryInterface,
    },
};

pub struct NotificationGenerationService {
    pub repo: Arc<dyn NotificationRepositoryInterface + Send + Sync>,
    pub email_template_engine: Arc<dyn NotificationTemplateEngineTrait + Send + Sync>,
    pub sms_template_engine: Arc<dyn NotificationTemplateEngineTrait + Send + Sync>,
}

impl NotificationGenerationService {
    pub fn create(
        notification_repository: Arc<dyn NotificationRepositoryInterface>,
        email_template_engine: Arc<dyn NotificationTemplateEngineTrait>,
        sms_template_engine: Arc<dyn NotificationTemplateEngineTrait>,
    ) -> Arc<dyn NotificationGenerationServiceTrait> {
        Arc::new(Self {
            repo: notification_repository,
            email_template_engine,
            sms_template_engine,
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

    pub async fn generate_email(
        &self, template: NotificationTemplate, data: HashMap<String, String>,
    ) -> NotificationContentDTO {
        NotificationContentDTO {
            subject: Some(self.email_template_engine.generate_subject(&template, &data)),
            message: self.email_template_engine.generate_message(&template, &data),
        }
    }

    async fn generate_sms(
        &self, template: NotificationTemplate, data: HashMap<String, String>,
    ) -> NotificationContentDTO {
        NotificationContentDTO {
            subject: None,
            message: self.sms_template_engine.generate_message(&template, &data),
        }
    }
}

#[async_trait]
impl NotificationGenerationServiceTrait for NotificationGenerationService {
    async fn generate_content(
        &self,
        notification_id: &str,
    ) -> Result<NotificationContentDTO, AppError> {
        let notification = match self._get_notification(&notification_id).await? {
            Some(notification) => notification,
            None => {
                return Err(AppError::NotFound(format!(
                    "Notification not found by id: {}",
                    notification_id
                )));
            }
        };
        let notification_content = match notification.channel {
            NotificationChannel::EMAIL => self.generate_email(notification.template, notification.data).await,
            NotificationChannel::SMS => self.generate_sms(notification.template, notification.data).await
        };
        return Ok(notification_content);
    }
}
