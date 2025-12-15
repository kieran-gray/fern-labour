use chrono::{DateTime, Utc};
use fern_labour_labour_shared::value_objects::{
    LabourUpdateType, SubscriberAccessLevel, SubscriberContactMethod, SubscriberRole,
};
use serde::{Deserialize, Serialize};
use std::fmt::Debug;
use uuid::Uuid;

use fern_labour_event_sourcing_rs::{Event, StoredEvent};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum LabourEvent {
    LabourPlanned {
        labour_id: Uuid,
        birthing_person_id: String,
        first_labour: bool,
        due_date: DateTime<Utc>,
        labour_name: Option<String>,
    },
    LabourPlanUpdated {
        labour_id: Uuid,
        first_labour: bool,
        due_date: DateTime<Utc>,
        labour_name: Option<String>,
    },
    LabourBegun {
        labour_id: Uuid,
        start_time: DateTime<Utc>,
    },
    LabourCompleted {
        labour_id: Uuid,
        notes: Option<String>,
        end_time: DateTime<Utc>,
    },
    LabourInviteSent {
        labour_id: Uuid,
        invite_email: String,
    },
    LabourDeleted {
        labour_id: Uuid,
    },
    ContractionStarted {
        labour_id: Uuid,
        contraction_id: Uuid,
        start_time: DateTime<Utc>,
    },
    ContractionEnded {
        labour_id: Uuid,
        contraction_id: Uuid,
        end_time: DateTime<Utc>,
        intensity: u8,
    },
    ContractionUpdated {
        labour_id: Uuid,
        contraction_id: Uuid,
        start_time: Option<DateTime<Utc>>,
        end_time: Option<DateTime<Utc>>,
        intensity: Option<u8>,
    },
    ContractionDeleted {
        labour_id: Uuid,
        contraction_id: Uuid,
    },
    LabourUpdatePosted {
        labour_id: Uuid,
        labour_update_id: Uuid,
        labour_update_type: LabourUpdateType,
        message: String,
        application_generated: bool,
        sent_time: DateTime<Utc>,
    },
    LabourUpdateMessageUpdated {
        labour_id: Uuid,
        labour_update_id: Uuid,
        message: String,
    },
    LabourUpdateTypeUpdated {
        labour_id: Uuid,
        labour_update_id: Uuid,
        labour_update_type: LabourUpdateType,
    },
    LabourUpdateDeleted {
        labour_id: Uuid,
        labour_update_id: Uuid,
    },
    SubscriberRequested {
        labour_id: Uuid,
        subscriber_id: String,
        subscription_id: Uuid,
    },
    SubscriberUnsubscribed {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    SubscriberNotificationMethodsUpdated {
        labour_id: Uuid,
        subscription_id: Uuid,
        notification_methods: Vec<SubscriberContactMethod>,
    },
    SubscriberAccessLevelUpdated {
        labour_id: Uuid,
        subscription_id: Uuid,
        access_level: SubscriberAccessLevel,
    },
    SubscriberApproved {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    SubscriberRemoved {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    SubscriberBlocked {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    SubscriberUnblocked {
        labour_id: Uuid,
        subscription_id: Uuid,
    },
    SubscriberRoleUpdated {
        labour_id: Uuid,
        subscription_id: Uuid,
        role: SubscriberRole,
    },
}

impl LabourEvent {
    pub fn into_stored_event(self) -> StoredEvent {
        let event_str = serde_json::to_string(&self).unwrap();

        StoredEvent {
            aggregate_id: self.aggregate_id().to_string(),
            event_type: self.event_type().to_string(),
            event_data: event_str,
            event_version: self.event_version(),
        }
    }

    pub fn from_stored_event(event: StoredEvent) -> Self {
        serde_json::from_str(&event.event_data).unwrap()
    }

    pub fn contraction_id(self) -> Option<Uuid> {
        match self {
            LabourEvent::ContractionStarted { contraction_id, .. } => Some(contraction_id),
            LabourEvent::ContractionEnded { contraction_id, .. } => Some(contraction_id),
            LabourEvent::ContractionUpdated { contraction_id, .. } => Some(contraction_id),
            LabourEvent::ContractionDeleted { contraction_id, .. } => Some(contraction_id),
            _ => None,
        }
    }

    pub fn labour_update_id(self) -> Option<Uuid> {
        match self {
            LabourEvent::LabourUpdatePosted {
                labour_update_id, ..
            } => Some(labour_update_id),
            LabourEvent::LabourUpdateMessageUpdated {
                labour_update_id, ..
            } => Some(labour_update_id),
            LabourEvent::LabourUpdateTypeUpdated {
                labour_update_id, ..
            } => Some(labour_update_id),
            LabourEvent::LabourUpdateDeleted {
                labour_update_id, ..
            } => Some(labour_update_id),
            _ => None,
        }
    }
}

impl Event for LabourEvent {
    fn event_type(&self) -> &str {
        match self {
            LabourEvent::LabourPlanned { .. } => "LabourPlanned",
            LabourEvent::LabourPlanUpdated { .. } => "LabourPlanUpdated",
            LabourEvent::LabourBegun { .. } => "LabourBegun",
            LabourEvent::LabourCompleted { .. } => "LabourCompleted",
            LabourEvent::LabourInviteSent { .. } => "LabourInviteSent",
            LabourEvent::LabourDeleted { .. } => "LabourDeleted",
            LabourEvent::ContractionStarted { .. } => "ContractionStarted",
            LabourEvent::ContractionEnded { .. } => "ContractionEnded",
            LabourEvent::ContractionUpdated { .. } => "ContractionUpdated",
            LabourEvent::ContractionDeleted { .. } => "ContractionDeleted",
            LabourEvent::LabourUpdatePosted { .. } => "LabourUpdatePosted",
            LabourEvent::LabourUpdateMessageUpdated { .. } => "LabourUpdateMessageUpdated",
            LabourEvent::LabourUpdateTypeUpdated { .. } => "LabourUpdateTypeUpdated",
            LabourEvent::LabourUpdateDeleted { .. } => "LabourUpdateDeleted",
            LabourEvent::SubscriberRequested { .. } => "SubscriberRequested",
            LabourEvent::SubscriberUnsubscribed { .. } => "SubscriberUnsubscribed",
            LabourEvent::SubscriberNotificationMethodsUpdated { .. } => {
                "SubscriberNotificationMethodsUpdated"
            }
            LabourEvent::SubscriberAccessLevelUpdated { .. } => "SubscriberAccessLevelUpdated",
            LabourEvent::SubscriberApproved { .. } => "SubscriberApproved",
            LabourEvent::SubscriberRemoved { .. } => "SubscriberRemoved",
            LabourEvent::SubscriberBlocked { .. } => "SubscriberBlocked",
            LabourEvent::SubscriberUnblocked { .. } => "SubscriberUnblocked",
            LabourEvent::SubscriberRoleUpdated { .. } => "SubscriberRoleUpdated",
        }
    }

    fn event_version(&self) -> i64 {
        1 // TODO: implement per event versioning
    }

    fn aggregate_id(&self) -> Uuid {
        match self {
            LabourEvent::LabourPlanned { labour_id, .. } => *labour_id,
            LabourEvent::LabourPlanUpdated { labour_id, .. } => *labour_id,
            LabourEvent::LabourBegun { labour_id, .. } => *labour_id,
            LabourEvent::LabourCompleted { labour_id, .. } => *labour_id,
            LabourEvent::LabourInviteSent { labour_id, .. } => *labour_id,
            LabourEvent::LabourDeleted { labour_id, .. } => *labour_id,
            LabourEvent::ContractionStarted { labour_id, .. } => *labour_id,
            LabourEvent::ContractionEnded { labour_id, .. } => *labour_id,
            LabourEvent::ContractionUpdated { labour_id, .. } => *labour_id,
            LabourEvent::ContractionDeleted { labour_id, .. } => *labour_id,
            LabourEvent::LabourUpdatePosted { labour_id, .. } => *labour_id,
            LabourEvent::LabourUpdateMessageUpdated { labour_id, .. } => *labour_id,
            LabourEvent::LabourUpdateTypeUpdated { labour_id, .. } => *labour_id,
            LabourEvent::LabourUpdateDeleted { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberRequested { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberUnsubscribed { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberNotificationMethodsUpdated { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberAccessLevelUpdated { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberApproved { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberRemoved { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberBlocked { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberUnblocked { labour_id, .. } => *labour_id,
            LabourEvent::SubscriberRoleUpdated { labour_id, .. } => *labour_id,
        }
    }
}
