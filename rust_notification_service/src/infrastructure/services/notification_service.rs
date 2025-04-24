use std::{collections::HashMap, str::FromStr};

use crate::{application::{dtos::NotificationDTO, exceptions::AppError}, domain::{
    entity::Notification, enums::{NotificationStatus, NotificationTemplate, NotificationType}, exceptions::InvalidNotificationStatus
}};

pub struct NotificationService;

impl NotificationService {
    pub async fn create_notification(
        &self,
        notification_type: String,
        destination: String,
        template: String,
        data: HashMap<String, String>,
        metadata: Option<HashMap<String, String>>,
        status: Option<String>,
    ) -> Result<NotificationDTO, AppError> {
        let notification_type = NotificationType::from_str(&notification_type);
        if let Err(error) = notification_type {
            return Err(AppError::ValidationError(error.to_string()))
        }
        let notification_type = notification_type.unwrap();
        
        let notification_status: Result<Option<NotificationStatus>, InvalidNotificationStatus> =
            Ok(None);
        if status.is_some() {
            let notification_status = NotificationStatus::from_str(&status.unwrap());
            if let Err(error) = notification_status {
                return Err(AppError::ValidationError(error.to_string()))
            }
        }
        let notification_status = notification_status.unwrap();

        let notification_template = NotificationTemplate::from_str(&template);
        if let Err(error) = notification_template {
            return Err(AppError::ValidationError(error.to_string()))
        }
        let notification_template = notification_template.unwrap();

        let notification = Notification::create(
            notification_type,
            destination,
            notification_template,
            data,
            notification_status,
            metadata,
        );

        // save in repo

        Ok(NotificationDTO::from(notification))
    }
}
