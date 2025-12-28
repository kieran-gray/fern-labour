use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
#[allow(non_camel_case_types)]
pub enum SubscriberRole {
    #[strum(serialize = "BIRTH_PARTNER", serialize = "birth_partner")]
    BIRTH_PARTNER,
    #[strum(serialize = "SUPPORT_PERSON", serialize = "support_person")]
    SUPPORT_PERSON,
    #[strum(serialize = "LOVED_ONE", serialize = "loved_one")]
    LOVED_ONE,
}

impl std::fmt::Display for SubscriberRole {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SubscriberRole::BIRTH_PARTNER => write!(f, "BIRTH_PARTNER"),
            SubscriberRole::SUPPORT_PERSON => write!(f, "SUPPORT_PERSON"),
            SubscriberRole::LOVED_ONE => write!(f, "LOVED_ONE"),
        }
    }
}
