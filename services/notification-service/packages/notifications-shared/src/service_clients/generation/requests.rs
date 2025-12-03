use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::value_objects::{NotificationChannel, NotificationTemplateData};

#[derive(Debug, Deserialize, Serialize)]
pub struct RenderRequest {
    pub notification_id: Uuid,
    pub channel: NotificationChannel,
    pub template_data: NotificationTemplateData,
}
