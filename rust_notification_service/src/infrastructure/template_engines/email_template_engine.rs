use std::{collections::HashMap, sync::Arc};

use crate::{
    application::services::template_engine::NotificationTemplateEngineTrait,
    domain::enums::NotificationTemplate,
};

pub struct EmailTemplateEngine;

impl EmailTemplateEngine {
    pub fn create() -> Arc<dyn NotificationTemplateEngineTrait> {
        Arc::new(Self)
    }
}

impl NotificationTemplateEngineTrait for EmailTemplateEngine {
    fn generate_subject(
        &self,
        template: &NotificationTemplate,
        data: &HashMap<String, String>,
    ) -> String {
        match template {
            NotificationTemplate::LABOUR_UPDATE => {
                let birthing_person_name = match data.get("birthing_person_name") {
                    Some(val) => val,
                    _ => &String::from("")
                };
                format!("Labour update from {birthing_person_name}")
            },
            NotificationTemplate::LABOUR_INVITE => String::from("Special invitation: Follow our baby's arrival journey 👶"),
            NotificationTemplate::SUBSCRIBER_INVITE => String::from("A Brilliant Way to Share Your Baby Journey! 🍼"),
            NotificationTemplate::CONTACT_US_SUBMISSION => {
                let email = match data.get("email") {
                    Some(val) => val,
                    _ => &String::from("")
                };
                format!("Contact us submission from: {email}")
            },
        }
    }

    fn generate_message(
        &self,
        template: &NotificationTemplate,
        data: &HashMap<String, String>,
    ) -> String {
        "Test".to_string()
    }
}
