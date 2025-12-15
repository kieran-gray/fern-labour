use serde::{Deserialize, Serialize};

#[derive(PartialEq, Debug, Deserialize, Serialize)]
pub struct CreateUserRequest {
    pub user_id: String,
    pub email: String,
    pub first_name: String,
    pub last_name: String,
    pub phone_number: Option<String>,
}

#[derive(PartialEq, Debug, Deserialize, Serialize)]
pub struct UpdateUserRequest {
    pub first_name: Option<String>,
    pub last_name: Option<String>,
    pub phone_number: Option<String>,
}
