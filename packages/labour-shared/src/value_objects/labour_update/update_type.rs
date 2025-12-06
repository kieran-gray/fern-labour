use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
#[allow(non_camel_case_types)]
pub enum LabourUpdateType {
    #[strum(serialize = "ANNOUNCEMENT", serialize = "announcement")]
    ANNOUNCEMENT,
    #[strum(serialize = "STATUS_UPDATE", serialize = "status_update")]
    STATUS_UPDATE,
    #[strum(serialize = "PRIVATE_NOTE", serialize = "private_note")]
    PRIVATE_NOTE,
}

impl std::fmt::Display for LabourUpdateType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LabourUpdateType::ANNOUNCEMENT => write!(f, "ANNOUNCEMENT"),
            LabourUpdateType::STATUS_UPDATE => write!(f, "STATUS_UPDATE"),
            LabourUpdateType::PRIVATE_NOTE => write!(f, "PRIVATE_NOTE"),
        }
    }
}
