use serde::{Deserialize, Serialize};
use std::cmp::Eq;
use strum::{EnumString, VariantNames};

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, VariantNames, PartialEq, Hash, Eq)]
#[allow(non_camel_case_types)]
pub enum SubscriberRole {
    #[strum(serialize = "BIRTH_PARTNER", serialize = "birth_partner")]
    BIRTH_PARTNER,
    #[strum(serialize = "FRIENDS_AND_FAMILY", serialize = "friends_and_family")]
    FRIENDS_AND_FAMILY,
}

impl std::fmt::Display for SubscriberRole {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SubscriberRole::BIRTH_PARTNER => write!(f, "BIRTH_PARTNER"),
            SubscriberRole::FRIENDS_AND_FAMILY => write!(f, "FRIENDS_AND_FAMILY"),
        }
    }
}
