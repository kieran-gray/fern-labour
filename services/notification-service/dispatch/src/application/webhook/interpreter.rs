use anyhow::{Result, anyhow};
use fern_labour_notifications_shared::value_objects::NotificationStatus;
use serde::Serialize;
use std::{collections::HashMap, rc::Rc};
use uuid::Uuid;

use crate::{
    application::webhook::ProviderStatusTranslator,
    domain::repository::TrackedNotificationRepositoryTrait,
};

#[derive(Serialize, Debug)]
pub struct WebhookInterpretation {
    pub notification_id: Uuid,
    pub status: NotificationStatus,
}

pub struct WebhookInterpreterService {
    repository: Rc<dyn TrackedNotificationRepositoryTrait>,
    translators: HashMap<String, Box<dyn ProviderStatusTranslator>>,
}

impl WebhookInterpreterService {
    pub fn create(
        repository: Rc<dyn TrackedNotificationRepositoryTrait>,
        translators: Vec<Box<dyn ProviderStatusTranslator>>,
    ) -> Self {
        let mut translator_map = HashMap::new();

        for translator in translators {
            translator_map.insert(translator.provider_name().to_string(), translator);
        }

        Self {
            repository,
            translators: translator_map,
        }
    }

    pub async fn interpret(
        &self,
        external_id: &str,
        provider_event: &str,
    ) -> Result<WebhookInterpretation> {
        let tracked = self.repository.get(external_id).await?;

        let translator = self.translators.get(&tracked.provider).ok_or_else(|| {
            anyhow!(
                "No status translator found for provider: {}. Available translators: {:?}",
                tracked.provider,
                self.translators.keys().collect::<Vec<_>>()
            )
        })?;

        let status = translator.translate(provider_event)?;

        Ok(WebhookInterpretation {
            notification_id: tracked.notification_id,
            status,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::tracked_notification::TrackedNotification;
    use anyhow::Result;
    use async_trait::async_trait;
    use chrono::Utc;
    use fern_labour_notifications_shared::value_objects::NotificationChannel;

    struct MockRepository {
        tracked: Option<TrackedNotification>,
    }

    #[async_trait(?Send)]
    impl TrackedNotificationRepositoryTrait for MockRepository {
        async fn get(&self, _external_id: &str) -> Result<TrackedNotification> {
            self.tracked.clone().ok_or_else(|| anyhow!("Not found"))
        }

        async fn put(&self, _tracked_notification: &TrackedNotification) -> Result<()> {
            Ok(())
        }
    }

    struct MockTranslator {
        provider: String,
    }

    impl ProviderStatusTranslator for MockTranslator {
        fn provider_name(&self) -> &str {
            &self.provider
        }

        fn translate(&self, event: &str) -> Result<NotificationStatus> {
            match event {
                "sent" => Ok(NotificationStatus::SENT),
                "delivered" => Ok(NotificationStatus::DELIVERED),
                "failed" => Ok(NotificationStatus::FAILED),
                _ => Err(anyhow!("Unknown event")),
            }
        }
    }

    #[tokio::test]
    async fn test_interpret_success() {
        let notification_id = Uuid::now_v7();
        let tracked = TrackedNotification {
            external_id: "ext123".to_string(),
            notification_id,
            channel: NotificationChannel::EMAIL,
            provider: "test-provider".to_string(),
            created_at: Utc::now(),
        };

        let repository = Rc::new(MockRepository {
            tracked: Some(tracked),
        });

        let translator = Box::new(MockTranslator {
            provider: "test-provider".to_string(),
        });

        let service = WebhookInterpreterService::create(repository, vec![translator]);

        let result = service.interpret("ext123", "delivered").await.unwrap();

        assert_eq!(result.notification_id, notification_id);
        assert_eq!(result.status, NotificationStatus::DELIVERED);
    }

    #[tokio::test]
    async fn test_interpret_unknown_provider() {
        let notification_id = Uuid::now_v7();
        let tracked = TrackedNotification {
            external_id: "ext123".to_string(),
            notification_id,
            channel: NotificationChannel::EMAIL,
            provider: "unknown-provider".to_string(),
            created_at: Utc::now(),
        };

        let repository = Rc::new(MockRepository {
            tracked: Some(tracked),
        });

        let translator = Box::new(MockTranslator {
            provider: "test-provider".to_string(),
        });

        let service = WebhookInterpreterService::create(repository, vec![translator]);

        let result = service.interpret("ext123", "delivered").await;

        assert!(result.is_err());
        assert!(
            result
                .unwrap_err()
                .to_string()
                .contains("No status translator found")
        );
    }
}
