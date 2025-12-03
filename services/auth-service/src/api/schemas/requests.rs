use serde::{Deserialize, Serialize};

#[derive(PartialEq, Debug, Deserialize, Serialize)]
pub struct VerifyTokenRequest {
    pub token: String,
}
