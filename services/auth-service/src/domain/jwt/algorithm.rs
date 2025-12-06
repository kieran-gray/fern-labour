use serde::{Deserialize, Serialize};
use strum::EnumString;

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, PartialEq)]
pub enum JwtAlgorithm {
    #[strum(serialize = "RS256", serialize = "rs256")]
    RS256,
}
