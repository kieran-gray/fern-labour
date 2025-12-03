use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationTemplateData, RenderedContent,
};
use tinytemplate::TinyTemplate;

use crate::{
    application::{exceptions::AppError, template_engine::TemplateEngineTrait},
    infrastructure::templates::{
        self,
        LabourAnnouncementTemplate,
        LabourBegunTemplate,
        LabourCompletedTemplate,
        LabourCompletedWithNoteTemplate,
        LabourUpdateTemplate,
        template::TemplateTrait,
    },
};

#[derive(Default)]
pub struct TinyTemplateEngine {}

impl TinyTemplateEngine {
    pub fn new() -> Self {
        Self {}
    }

    fn render_subject<T: TemplateTrait>(
        &self,
        template_name: &str,
        data: &NotificationTemplateData,
    ) -> Result<String, AppError> {
        let mut tt = TinyTemplate::new();

        let template_text = T::template_string();

        tt.add_template(template_name, template_text)
            .map_err(|e| AppError::InternalError(e.to_string()))?;

        let rendered = tt
            .render(template_name, data)
            .map_err(|e| AppError::InternalError(e.to_string()))?;

        Ok(rendered)
    }

    fn render_body<T: TemplateTrait>(
        &self,
        template_name: &str,
        data: &NotificationTemplateData,
    ) -> Result<String, AppError> {
        let mut tt = TinyTemplate::new();

        let template_text = T::template_string();

        tt.add_template(template_name, template_text)
            .map_err(|e| AppError::InternalError(e.to_string()))?;

        let rendered = tt
            .render(template_name, data)
            .map_err(|e| AppError::InternalError(e.to_string()))?;

        Ok(rendered)
    }
}

impl TemplateEngineTrait for TinyTemplateEngine {
    fn render_content(
        &self,
        channel: NotificationChannel,
        data: NotificationTemplateData,
    ) -> Result<RenderedContent, AppError> {
        match data {
            data @ NotificationTemplateData::ContactUs { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self
                        .render_subject::<templates::ContactUsSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::ContactUsBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourAnnouncementData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourAnnouncementSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::LabourAnnouncementBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<LabourAnnouncementTemplate>(data.template(), &data)?,
                }),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourBegunData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourBegunSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::LabourBegunBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<LabourBegunTemplate>(data.template(), &data)?,
                }),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourCompletedData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourCompletedSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::LabourCompletedBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<LabourCompletedTemplate>(data.template(), &data)?,
                }),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourCompletedWithNoteData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourCompletedWithNoteSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::LabourCompletedWithNoteBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<LabourCompletedWithNoteTemplate>(data.template(), &data)?,
                }),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourUpdateData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourUpdateSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::LabourUpdateBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<LabourUpdateTemplate>(data.template(), &data)?,
                }),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourInviteData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourInviteSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::LabourInviteBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::SubscriberInviteData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::SubscriberInviteSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::SubscriberInviteBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::SubscriberRequestedData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::SubscriberRequestedSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::SubscriberRequestedBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::SubscriberApprovedData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::SubscriberApprovedSubjectTemplate>(data.template(), &data)?,
                    html_body: self.render_body::<templates::SubscriberApprovedBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                _ => Err(AppError::ValidationError(format!(
                    "Unknown channel {channel}"
                ))),
            },
        }
    }
}
