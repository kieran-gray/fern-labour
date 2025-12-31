use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationTemplateData, RenderedContent,
};
use tinytemplate::TinyTemplate;

use crate::{
    application::{exceptions::AppError, template_engine::TemplateEngineTrait},
    infrastructure::templates::{self, template::TemplateTrait},
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
                    subject: self.render_subject::<templates::ContactUsSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self
                        .render_body::<templates::ContactUsBodyTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                NotificationChannel::WHATSAPP => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourAnnouncementData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourAnnouncementSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::LabourAnnouncementBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<templates::sms_templates::labour_announcement::LabourAnnouncementTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::WHATSAPP => Ok(RenderedContent::WhatsApp {
                    template_sid: self.render_subject::<templates::whatsapp_templates::labour_announcement::LabourAnnouncementTemplateSid>(data.template(), &data)?,
                    content_variables: self.render_body::<templates::whatsapp_templates::labour_announcement::LabourAnnouncementContentVariablesTemplate>(data.template(), &data)?,
                }),
            },
            data @ NotificationTemplateData::LabourBegunData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourBegunSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::LabourBegunBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<templates::sms_templates::labour_begun::LabourBegunTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::WHATSAPP => Ok(RenderedContent::WhatsApp {
                    template_sid: self.render_subject::<templates::whatsapp_templates::labour_begun::LabourBegunTemplateSid>(data.template(), &data)?,
                    content_variables: self.render_body::<templates::whatsapp_templates::labour_begun::LabourBegunContentVariablesTemplate>(data.template(), &data)?,
                }),
            },
            data @ NotificationTemplateData::LabourCompletedData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourCompletedSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::LabourCompletedBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<templates::sms_templates::labour_completed::LabourCompletedTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::WHATSAPP => Ok(RenderedContent::WhatsApp {
                    template_sid: self.render_subject::<templates::whatsapp_templates::labour_completed::LabourCompletedTemplateSid>(data.template(), &data)?,
                    content_variables: self.render_body::<templates::whatsapp_templates::labour_completed::LabourCompletedContentVariablesTemplate>(data.template(), &data)?,
                }),
            },
            data @ NotificationTemplateData::LabourCompletedWithNoteData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self
                        .render_subject::<templates::LabourCompletedWithNoteSubjectTemplate>(
                            data.template(),
                            &data,
                        )?,
                    html_body: self.render_body::<templates::LabourCompletedWithNoteBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self
                        .render_body::<templates::sms_templates::labour_completed_with_note::LabourCompletedWithNoteTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::WHATSAPP => Ok(RenderedContent::WhatsApp {
                    template_sid: self.render_subject::<templates::whatsapp_templates::labour_completed_with_note::LabourCompletedWithNoteTemplateSid>(data.template(), &data)?,
                    content_variables: self.render_body::<templates::whatsapp_templates::labour_completed_with_note::LabourCompletedWithNoteContentVariablesTemplate>(data.template(), &data)?,
                }),
            },
            data @ NotificationTemplateData::LabourUpdateData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourUpdateSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::LabourUpdateBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Ok(RenderedContent::Sms {
                    body: self.render_body::<templates::sms_templates::labour_update::LabourUpdateTemplate>(data.template(), &data)?,
                }),
                NotificationChannel::WHATSAPP => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::LabourInviteData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::LabourInviteSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::LabourInviteBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                NotificationChannel::WHATSAPP => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::SubscriberInviteData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::SubscriberInviteSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::SubscriberInviteBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                NotificationChannel::WHATSAPP => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::SubscriberRequestedData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::SubscriberRequestedSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::SubscriberRequestedBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                NotificationChannel::WHATSAPP => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
            },
            data @ NotificationTemplateData::SubscriberApprovedData { .. } => match channel {
                NotificationChannel::EMAIL => Ok(RenderedContent::Email {
                    subject: self.render_subject::<templates::SubscriberApprovedSubjectTemplate>(
                        data.template(),
                        &data,
                    )?,
                    html_body: self.render_body::<templates::SubscriberApprovedBodyTemplate>(
                        data.template(),
                        &data,
                    )?,
                }),
                NotificationChannel::SMS => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
                NotificationChannel::WHATSAPP => Err(AppError::ValidationError(format!(
                    "Template not found for channel {channel}"
                ))),
            },
        }
    }
}
