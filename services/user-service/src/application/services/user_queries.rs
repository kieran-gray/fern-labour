use std::sync::Arc;

use async_trait::async_trait;

use crate::{
    application::{dtos::UserDTO, exceptions::AppError},
    domain::{repository::UserRepository as UserRepositoryInterface, value_objects::UserId},
};

#[async_trait(?Send)]
pub trait UserQueryServiceTrait {
    /// Get user by ID
    async fn get_user_by_id(&self, user_id: String) -> Result<UserDTO, AppError>;

    /// Get user by email (for Auth0 sync checks)
    async fn get_user_by_email(&self, email: String) -> Result<Option<UserDTO>, AppError>;

    /// Check if user exists
    async fn user_exists(&self, user_id: String) -> Result<bool, AppError>;
}

pub struct UserQueryService {
    pub repo: Arc<dyn UserRepositoryInterface + Send + Sync>,
}

impl UserQueryService {
    pub fn create(user_repo: Arc<dyn UserRepositoryInterface>) -> Arc<Self> {
        Arc::new(Self { repo: user_repo })
    }
}

#[async_trait(?Send)]
impl UserQueryServiceTrait for UserQueryService {
    async fn get_user_by_id(&self, user_id: String) -> Result<UserDTO, AppError> {
        let id =
            UserId::new(user_id.clone()).map_err(|e| AppError::ValidationError(e.to_string()))?;

        let user = self
            .repo
            .get_by_id(&id)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to get user: {e}")))?
            .ok_or_else(|| AppError::NotFound(format!("User with ID {} not found", user_id)))?;

        Ok(UserDTO::from(user))
    }

    async fn get_user_by_email(&self, email: String) -> Result<Option<UserDTO>, AppError> {
        let user =
            self.repo.get_by_email(&email).await.map_err(|e| {
                AppError::DatabaseError(format!("Failed to get user by email: {e}"))
            })?;

        Ok(user.map(UserDTO::from))
    }

    async fn user_exists(&self, user_id: String) -> Result<bool, AppError> {
        let id = UserId::new(user_id).map_err(|e| AppError::ValidationError(e.to_string()))?;

        self.repo
            .exists(&id)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to check user existence: {e}")))
    }
}
