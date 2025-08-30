use std::{collections::HashMap, sync::Arc};

use crate::{
    application::services::template_engine::NotificationTemplateEngineTrait,
    domain::enums::NotificationTemplate,
};

pub struct SMSTemplateEngine;

impl SMSTemplateEngine {
    pub fn create() -> Arc<dyn NotificationTemplateEngineTrait> {
        Arc::new(Self)
    }
}

impl NotificationTemplateEngineTrait for SMSTemplateEngine {
    fn generate_subject(
        &self,
        _template: &NotificationTemplate,
        _data: &HashMap<String, String>,
    ) -> String {
        String::from("")
    }

    fn generate_message(
        &self,
        template: &NotificationTemplate,
        data: &HashMap<String, String>,
    ) -> String {
        match template { // TODO: try to use struct for data instead
            NotificationTemplate::LABOUR_UPDATE => {
                let subscriber_first_name = match data.get("subscriber_first_name") {
                    Some(val) => val,
                    _ => &String::from("")
                };
                let update = match data.get("update") {
                    Some(val) => val,
                    _ => &String::from("")
                };
                format!("Hey {}, {}", subscriber_first_name, update)
            },
            _ => String::from("")
        }
    }
}
