use fern_labour_notifications_shared::value_objects::{
    NotificationChannel, NotificationTemplateData, RenderedContent,
};

use crate::application::exceptions::AppError;

pub trait TemplateEngineTrait {
    fn render_content(
        &self,
        channel: NotificationChannel,
        data: NotificationTemplateData,
    ) -> Result<RenderedContent, AppError>;
}
