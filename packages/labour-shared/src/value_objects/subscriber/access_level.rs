use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
pub enum SubscriberAccessLevel {
    #[strum(serialize = "BASIC", serialize = "basic")]
    BASIC,
    #[strum(serialize = "SUPPORTER", serialize = "supporter")]
    SUPPORTER,
}

impl std::fmt::Display for SubscriberAccessLevel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SubscriberAccessLevel::BASIC => write!(f, "BASIC"),
            SubscriberAccessLevel::SUPPORTER => write!(f, "SUPPORTER"),
        }
    }
}
