use crate::domain::entity::User;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserDTO {
    pub id: String,
    pub email: String,
    pub first_name: String,
    pub last_name: String,
    pub phone_number: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl From<User> for UserDTO {
    fn from(user: User) -> Self {
        Self {
            id: user.id.value().to_string(),
            email: user.email.value().to_string(),
            first_name: user.first_name,
            last_name: user.last_name,
            phone_number: user.phone_number.map(|p| p.value().to_string()),
            created_at: user.created_at.to_rfc3339(),
            updated_at: user.updated_at.to_rfc3339(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateUserRequest {
    pub user_id: String,
    pub email: String,
    pub first_name: String,
    pub last_name: String,
    pub phone_number: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateUserRequest {
    pub first_name: Option<String>,
    pub last_name: Option<String>,
    pub phone_number: Option<String>,
}
