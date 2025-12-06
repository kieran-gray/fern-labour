use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum RenderedContent {
    Email { subject: String, html_body: String },
    Sms { body: String },
    WhatsApp { body: String },
}

impl RenderedContent {
    pub fn channel(&self) -> &str {
        match self {
            RenderedContent::Email { .. } => "EMAIL",
            RenderedContent::Sms { .. } => "SMS",
            RenderedContent::WhatsApp { .. } => "WHATSAPP",
        }
    }

    pub fn has_subject(&self) -> bool {
        matches!(self, RenderedContent::Email { .. })
    }

    pub fn body(&self) -> &str {
        match self {
            RenderedContent::Email { html_body, .. } => html_body,
            RenderedContent::Sms { body } => body,
            RenderedContent::WhatsApp { body } => body,
        }
    }

    pub fn subject(&self) -> Option<&str> {
        match self {
            RenderedContent::Email { subject, .. } => Some(subject),
            _ => None,
        }
    }
}
