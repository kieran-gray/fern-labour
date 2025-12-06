use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
pub enum NotificationPriority {
    #[serde(rename = "normal")]
    #[default]
    Normal,
    #[serde(rename = "high")]
    High,
}

impl fmt::Display for NotificationPriority {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            NotificationPriority::Normal => write!(f, "normal"),
            NotificationPriority::High => write!(f, "high"),
        }
    }
}

impl NotificationPriority {
    pub fn is_high(&self) -> bool {
        matches!(self, NotificationPriority::High)
    }

    pub fn is_normal(&self) -> bool {
        matches!(self, NotificationPriority::Normal)
    }
}
