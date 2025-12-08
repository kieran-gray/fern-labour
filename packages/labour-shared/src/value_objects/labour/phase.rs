use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
#[allow(non_camel_case_types)]
pub enum LabourPhase {
    #[strum(serialize = "PLANNED", serialize = "planned")]
    PLANNED,
    #[strum(serialize = "EARLY", serialize = "early")]
    EARLY,
    #[strum(serialize = "ACTIVE", serialize = "active")]
    ACTIVE,
    #[strum(serialize = "TRANSITION", serialize = "transition")]
    TRANSITION,
    #[strum(serialize = "PUSHING", serialize = "pushing")]
    PUSHING,
    #[strum(serialize = "COMPLETE", serialize = "complete")]
    COMPLETE,
}

impl std::fmt::Display for LabourPhase {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LabourPhase::PLANNED => write!(f, "PLANNED"),
            LabourPhase::EARLY => write!(f, "EARLY"),
            LabourPhase::ACTIVE => write!(f, "ACTIVE"),
            LabourPhase::TRANSITION => write!(f, "TRANSITION"),
            LabourPhase::PUSHING => write!(f, "PUSHING"),
            LabourPhase::COMPLETE => write!(f, "COMPLETE"),
        }
    }
}
