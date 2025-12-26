use serde::{Deserialize, Serialize};
use std::cmp::{Eq, Ordering};
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

impl LabourPhase {
    fn ordinal(&self) -> u8 {
        match self {
            LabourPhase::PLANNED => 0,
            LabourPhase::EARLY => 1,
            LabourPhase::ACTIVE => 2,
            LabourPhase::TRANSITION => 3,
            LabourPhase::PUSHING => 4,
            LabourPhase::COMPLETE => 5,
        }
    }
}

impl PartialOrd for LabourPhase {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for LabourPhase {
    fn cmp(&self, other: &Self) -> Ordering {
        self.ordinal().cmp(&other.ordinal())
    }
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
