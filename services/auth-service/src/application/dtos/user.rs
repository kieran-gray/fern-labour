use serde::{Deserialize, Serialize};

use crate::domain::AuthenticatedPrincipal;

#[derive(PartialEq, Debug, Deserialize, Serialize)]
pub struct UserDto {
    pub user_id: String,
    pub issuer: String,
    pub email: Option<String>,
    pub email_verified: Option<bool>,
    pub name: Option<String>,
}

impl From<AuthenticatedPrincipal> for UserDto {
    fn from(value: AuthenticatedPrincipal) -> Self {
        Self {
            user_id: value.identity_id,
            issuer: value.issuer,
            email: value.email,
            email_verified: value.email_verified,
            name: value.name,
        }
    }
}
