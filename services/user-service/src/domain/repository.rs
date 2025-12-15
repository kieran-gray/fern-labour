use super::entity::User;
use super::exceptions::RepositoryError;
use super::value_objects::UserId;

use async_trait::async_trait;

#[async_trait(?Send)]
pub trait UserRepository: Send + Sync {
    async fn save(&self, user: &User) -> Result<(), RepositoryError>;

    async fn get_by_id(&self, user_id: &UserId) -> Result<Option<User>, RepositoryError>;

    async fn get_by_email(&self, email: &str) -> Result<Option<User>, RepositoryError>;

    async fn exists(&self, user_id: &UserId) -> Result<bool, RepositoryError>;

    async fn delete(&self, user_id: &UserId) -> Result<(), RepositoryError>;
}
