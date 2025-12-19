use anyhow::{Context, Result};

use fern_labour_workers_shared::User;

use crate::durable_object::security::user_storage::UserStorage;

pub struct UserQuery {
    user_storage: UserStorage,
}

impl UserQuery {
    pub fn new(user_storage: UserStorage) -> Self {
        Self { user_storage }
    }

    pub fn get_users(&self) -> Result<Vec<User>> {
        let users = self.user_storage.get().context("Failed to get users")?;

        Ok(users)
    }

    pub fn get_user_by_id(&self, user_id: String) -> Result<Vec<User>> {
        let user = self
            .user_storage
            .get_user(&user_id)
            .context("Failed to get users")?;

        Ok(user)
    }
}
