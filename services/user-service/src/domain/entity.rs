use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

use crate::domain::exceptions::ValidationError;
use crate::domain::value_objects::{Email, PhoneNumber, UserId};

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct User {
    pub id: UserId,
    pub email: Email,
    pub first_name: String,
    pub last_name: String,
    pub phone_number: Option<PhoneNumber>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl User {
    pub fn create(
        user_id: String,
        email: String,
        first_name: String,
        last_name: String,
        phone_number: Option<String>,
    ) -> Result<Self, ValidationError> {
        let id = UserId::new(user_id)?;
        let email = Email::new(email)?;
        Self::validate_first_name(&first_name)?;
        Self::validate_last_name(&last_name)?;

        let phone_number = match phone_number {
            Some(phone) if !phone.trim().is_empty() => Some(PhoneNumber::new(phone)?),
            _ => None,
        };

        let now = Utc::now();

        Ok(Self {
            id,
            email,
            first_name: first_name.trim().to_string(),
            last_name: last_name.trim().to_string(),
            phone_number,
            created_at: now,
            updated_at: now,
        })
    }

    pub fn update_profile(
        &mut self,
        first_name: Option<String>,
        last_name: Option<String>,
        phone_number: Option<String>,
    ) -> Result<(), ValidationError> {
        if let Some(first_name) = first_name {
            Self::validate_first_name(&first_name)?;
            self.first_name = first_name.trim().to_string();
        }

        if let Some(last_name) = last_name {
            Self::validate_last_name(&last_name)?;
            self.last_name = last_name.trim().to_string();
        }

        if let Some(phone) = phone_number {
            self.phone_number = if phone.trim().is_empty() {
                None
            } else {
                Some(PhoneNumber::new(phone)?)
            };
        }

        self.updated_at = Utc::now();
        Ok(())
    }

    fn validate_first_name(name: &str) -> Result<(), ValidationError> {
        let trimmed = name.trim();

        if trimmed.is_empty() {
            return Err(ValidationError::InvalidFirstName(
                "First name cannot be empty".into(),
            ));
        }

        if trimmed.len() > 100 {
            return Err(ValidationError::InvalidFirstName(
                "First name must be 100 characters or less".into(),
            ));
        }

        Ok(())
    }

    fn validate_last_name(name: &str) -> Result<(), ValidationError> {
        let trimmed = name.trim();

        if trimmed.is_empty() {
            return Err(ValidationError::InvalidLastName(
                "Last name cannot be empty".into(),
            ));
        }

        if trimmed.len() > 100 {
            return Err(ValidationError::InvalidLastName(
                "Last name must be 100 characters or less".into(),
            ));
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_valid_user() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            Some("+1234567890".to_string()),
        );

        assert!(result.is_ok());
        let user = result.unwrap();
        assert_eq!(user.email.value(), "test@example.com");
        assert_eq!(user.first_name, "John");
        assert_eq!(user.last_name, "Doe");
        assert!(user.phone_number.is_some());
    }

    #[test]
    fn test_create_user_without_phone() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            None,
        );

        assert!(result.is_ok());
        let user = result.unwrap();
        assert!(user.phone_number.is_none());
    }

    #[test]
    fn test_create_user_with_empty_phone() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            Some("   ".to_string()),
        );

        assert!(result.is_ok());
        let user = result.unwrap();
        assert!(user.phone_number.is_none());
    }

    #[test]
    fn test_create_user_trims_names() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "  John  ".to_string(),
            "  Doe  ".to_string(),
            None,
        );

        assert!(result.is_ok());
        let user = result.unwrap();
        assert_eq!(user.first_name, "John");
        assert_eq!(user.last_name, "Doe");
    }

    #[test]
    fn test_create_user_invalid_email() {
        let result = User::create(
            "test-user".to_string(),
            "invalid-email".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            None,
        );

        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            ValidationError::InvalidEmail(_)
        ));
    }

    #[test]
    fn test_create_user_empty_first_name() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "".to_string(),
            "Doe".to_string(),
            None,
        );

        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            ValidationError::InvalidFirstName(_)
        ));
    }

    #[test]
    fn test_create_user_empty_last_name() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "   ".to_string(),
            None,
        );

        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            ValidationError::InvalidLastName(_)
        ));
    }

    #[test]
    fn test_create_user_first_name_too_long() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "a".repeat(101),
            "Doe".to_string(),
            None,
        );

        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            ValidationError::InvalidFirstName(_)
        ));
    }

    #[test]
    fn test_create_user_last_name_too_long() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "a".repeat(101),
            None,
        );

        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            ValidationError::InvalidLastName(_)
        ));
    }

    #[test]
    fn test_create_user_invalid_phone() {
        let result = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            Some("123".to_string()),
        );

        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            ValidationError::InvalidPhoneNumber(_)
        ));
    }

    #[test]
    fn test_update_profile_first_name() {
        let mut user = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            None,
        )
        .unwrap();

        let result = user.update_profile(Some("Jane".to_string()), None, None);
        assert!(result.is_ok());
        assert_eq!(user.first_name, "Jane");
    }

    #[test]
    fn test_update_profile_last_name() {
        let mut user = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            None,
        )
        .unwrap();

        let result = user.update_profile(None, Some("Smith".to_string()), None);
        assert!(result.is_ok());
        assert_eq!(user.last_name, "Smith");
    }

    #[test]
    fn test_update_profile_phone_number() {
        let mut user = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            None,
        )
        .unwrap();

        let result = user.update_profile(None, None, Some("+1234567890".to_string()));
        assert!(result.is_ok());
        assert!(user.phone_number.is_some());
        assert_eq!(user.phone_number.unwrap().value(), "+1234567890");
    }

    #[test]
    fn test_update_profile_remove_phone() {
        let mut user = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            Some("+1234567890".to_string()),
        )
        .unwrap();

        let result = user.update_profile(None, None, Some("".to_string()));
        assert!(result.is_ok());
        assert!(user.phone_number.is_none());
    }

    #[test]
    fn test_update_profile_invalid_first_name() {
        let mut user = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            None,
        )
        .unwrap();

        let result = user.update_profile(Some("".to_string()), None, None);
        assert!(result.is_err());
        assert!(matches!(
            result.unwrap_err(),
            ValidationError::InvalidFirstName(_)
        ));
    }

    #[test]
    fn test_update_profile_updates_timestamp() {
        let mut user = User::create(
            "test-user".to_string(),
            "test@example.com".to_string(),
            "John".to_string(),
            "Doe".to_string(),
            None,
        )
        .unwrap();

        let original_updated_at = user.updated_at;

        // Sleep briefly to ensure timestamp difference
        std::thread::sleep(std::time::Duration::from_millis(10));

        user.update_profile(Some("Jane".to_string()), None, None)
            .unwrap();

        assert!(user.updated_at > original_updated_at);
    }
}
