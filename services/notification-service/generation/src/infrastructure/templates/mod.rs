pub mod email_templates;
pub mod sms_templates;
pub mod template;

pub use email_templates::contact_us::{ContactUsBodyTemplate, ContactUsSubjectTemplate};
pub use email_templates::labour_announcement::{
    LabourAnnouncementBodyTemplate, LabourAnnouncementSubjectTemplate,
};
pub use email_templates::labour_begun::{LabourBegunBodyTemplate, LabourBegunSubjectTemplate};
pub use email_templates::labour_completed::{
    LabourCompletedBodyTemplate, LabourCompletedSubjectTemplate,
};
pub use email_templates::labour_completed_with_note::{
    LabourCompletedWithNoteBodyTemplate, LabourCompletedWithNoteSubjectTemplate,
};
pub use email_templates::labour_invite::{LabourInviteBodyTemplate, LabourInviteSubjectTemplate};
pub use email_templates::labour_update::{LabourUpdateBodyTemplate, LabourUpdateSubjectTemplate};
pub use email_templates::subscriber_approved::{
    SubscriberApprovedBodyTemplate, SubscriberApprovedSubjectTemplate,
};
pub use email_templates::subscriber_invite::{
    SubscriberInviteBodyTemplate, SubscriberInviteSubjectTemplate,
};
pub use email_templates::subscriber_requested::{
    SubscriberRequestedBodyTemplate, SubscriberRequestedSubjectTemplate,
};

pub use sms_templates::labour_announcement::LabourAnnouncementTemplate;
pub use sms_templates::labour_begun::LabourBegunTemplate;
pub use sms_templates::labour_completed::LabourCompletedTemplate;
pub use sms_templates::labour_completed_with_note::LabourCompletedWithNoteTemplate;
pub use sms_templates::labour_update::LabourUpdateTemplate;