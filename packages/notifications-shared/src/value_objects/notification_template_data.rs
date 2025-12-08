use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(tag = "type")]
pub enum NotificationTemplateData {
    ContactUs {
        name: String,
    },
    LabourUpdateData {
        birthing_person_name: String,
        subscriber_first_name: String,
        update: String,
        link: String,
        notes: Option<String>,
    },
    LabourAnnouncementData {
        birthing_person_name: String,
        birthing_person_first_name: String,
        subscriber_first_name: String,
        announcement: String,
        link: String,
    },
    LabourBegunData {
        birthing_person_name: String,
        birthing_person_first_name: String,
        subscriber_first_name: String,
        link: String,
    },
    LabourCompletedData {
        birthing_person_name: String,
        birthing_person_first_name: String,
        subscriber_first_name: String,
        link: String,
    },
    LabourCompletedWithNoteData {
        birthing_person_name: String,
        birthing_person_first_name: String,
        subscriber_first_name: String,
        update: String,
        link: String,
    },
    LabourInviteData {
        birthing_person_name: String,
        birthing_person_first_name: String,
        link: String,
    },
    SubscriberInviteData {
        subscriber_name: String,
        link: String,
    },
    SubscriberRequestedData {
        birthing_person_first_name: String,
        subscriber_name: String,
        link: String,
    },
    SubscriberApprovedData {
        subscriber_first_name: String,
        birthing_person_name: String,
        link: String,
    },
}

impl NotificationTemplateData {
    pub fn template(&self) -> &str {
        match self {
            NotificationTemplateData::ContactUs { .. } => "ContactUs",
            NotificationTemplateData::LabourUpdateData { .. } => "LabourUpdateData",
            NotificationTemplateData::LabourAnnouncementData { .. } => "LabourAnnouncementData",
            NotificationTemplateData::LabourBegunData { .. } => "LabourBegunData",
            NotificationTemplateData::LabourCompletedData { .. } => "LabourCompletedData",
            NotificationTemplateData::LabourCompletedWithNoteData { .. } => {
                "LabourCompletedWithNoteData"
            }
            NotificationTemplateData::LabourInviteData { .. } => "LabourInviteData",
            NotificationTemplateData::SubscriberInviteData { .. } => "SubscriberInviteData",
            NotificationTemplateData::SubscriberRequestedData { .. } => "SubscriberRequestedData",
            NotificationTemplateData::SubscriberApprovedData { .. } => "SubscriberApprovedData",
        }
    }
}
