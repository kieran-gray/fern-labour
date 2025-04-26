use std::collections::HashMap;

use crate::domain::enums::NotificationTemplate;

pub trait NotificationTemplateEngineTrait: Send + Sync {
    fn generate_subject(
        &self,
        template: &NotificationTemplate,
        data: &HashMap<String, String>,
    ) -> String;

    fn generate_message(
        &self,
        template: &NotificationTemplate,
        data: &HashMap<String, String>,
    ) -> String;
}
