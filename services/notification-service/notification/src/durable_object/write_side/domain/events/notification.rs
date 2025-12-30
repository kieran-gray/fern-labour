use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationDestination, NotificationPriority, NotificationTemplateData,
    RenderedContent,
};
use serde::{Deserialize, Serialize};
use std::{collections::HashMap, fmt::Debug};
use uuid::Uuid;

use fern_labour_event_sourcing_rs::{Event, impl_event};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct NotificationRequested {
    pub notification_id: Uuid,
    pub channel: NotificationChannel,
    pub destination: NotificationDestination,
    pub template_data: NotificationTemplateData,
    pub metadata: Option<HashMap<String, String>>,
    pub priority: NotificationPriority,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct RenderedContentStored {
    pub notification_id: Uuid,
    pub rendered_content: RenderedContent,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct NotificationDispatched {
    pub notification_id: Uuid,
    pub external_id: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct NotificationDelivered {
    pub notification_id: Uuid,
    pub external_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct NotificationDeliveryFailed {
    pub notification_id: Uuid,
    pub external_id: String,
    pub reason: Option<String>,
}

impl_event!(NotificationRequested, notification_id);
impl_event!(RenderedContentStored, notification_id);
impl_event!(NotificationDispatched, notification_id);
impl_event!(NotificationDelivered, notification_id);
impl_event!(NotificationDeliveryFailed, notification_id);
