use std::sync::Arc;

use async_trait::async_trait;

use crate::{
    application::{
        dtos::{CreateUserRequest, UpdateUserRequest},
        exceptions::AppError,
    },
    domain::{
        entity::User, repository::UserRepository as UserRepositoryInterface, value_objects::UserId,
    },
};

#[async_trait(?Send)]
pub trait UserCommandServiceTrait {
    async fn create_user(&self, request: CreateUserRequest) -> Result<(), AppError>;

    async fn update_user(
        &self,
        user_id: String,
        request: UpdateUserRequest,
    ) -> Result<(), AppError>;

    async fn delete_user(&self, user_id: String) -> Result<(), AppError>;
}

pub struct UserCommandService {
    pub repo: Arc<dyn UserRepositoryInterface + Send + Sync>,
}

impl UserCommandService {
    pub fn create(user_repo: Arc<dyn UserRepositoryInterface>) -> Arc<Self> {
        Arc::new(Self { repo: user_repo })
    }
}

#[async_trait(?Send)]
impl UserCommandServiceTrait for UserCommandService {
    async fn create_user(&self, request: CreateUserRequest) -> Result<(), AppError> {
        let user_id = UserId::new(request.user_id.clone())
            .map_err(|e| AppError::ValidationError(e.to_string()))?;

        if self
            .repo
            .exists(&user_id)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to check user existence: {e}")))?
        {
            return Err(AppError::ValidationError(format!(
                "User with ID {} already exists",
                request.user_id
            )));
        }

        let user = User::create(
            request.user_id,
            request.email,
            request.first_name,
            request.last_name,
            request.phone_number,
        )
        .map_err(|e| AppError::ValidationError(e.to_string()))?;

        self.repo
            .save(&user)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to save user: {e}")))?;

        Ok(())
    }

    async fn update_user(
        &self,
        user_id: String,
        request: UpdateUserRequest,
    ) -> Result<(), AppError> {
        let id =
            UserId::new(user_id.clone()).map_err(|e| AppError::ValidationError(e.to_string()))?;

        let mut user = self
            .repo
            .get_by_id(&id)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to get user: {e}")))?
            .ok_or_else(|| AppError::NotFound(format!("User with ID {} not found", user_id)))?;

        user.update_profile(request.first_name, request.last_name, request.phone_number)
            .map_err(|e| AppError::ValidationError(e.to_string()))?;

        self.repo
            .save(&user)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to update user: {e}")))?;

        Ok(())
    }

    async fn delete_user(&self, user_id: String) -> Result<(), AppError> {
        let id =
            UserId::new(user_id.clone()).map_err(|e| AppError::ValidationError(e.to_string()))?;

        if !self
            .repo
            .exists(&id)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to check user existence: {e}")))?
        {
            return Err(AppError::NotFound(format!(
                "User with ID {} not found",
                user_id
            )));
        }

        self.repo
            .delete(&id)
            .await
            .map_err(|e| AppError::DatabaseError(format!("Failed to delete user: {e}")))?;

        Ok(())
    }
}
