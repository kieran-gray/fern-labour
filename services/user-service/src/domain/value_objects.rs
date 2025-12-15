use regex::Regex;
use serde::{Deserialize, Serialize};

use crate::domain::exceptions::ValidationError;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UserId(String);

impl UserId {
    pub fn new(id: String) -> Result<Self, ValidationError> {
        if id.is_empty() {
            return Err(ValidationError::InvalidUserId(
                "User ID cannot be empty".into(),
            ));
        }
        Ok(Self(id))
    }

    pub fn value(&self) -> &str {
        &self.0
    }
}

impl From<String> for UserId {
    fn from(id: String) -> Self {
        Self(id)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Email(String);

impl Email {
    pub fn new(email: String) -> Result<Self, ValidationError> {
        Self::validate(&email)?;
        Ok(Self(email))
    }

    fn validate(email: &str) -> Result<(), ValidationError> {
        if email.is_empty() || email.len() > 254 {
            return Err(ValidationError::InvalidEmail(
                "Email must be between 1 and 254 characters".into(),
            ));
        }

        let email_regex = Regex::new(r"^[^\s@]+@[^\s@]+\.[^\s@]+$").unwrap();
        if !email_regex.is_match(email) {
            return Err(ValidationError::InvalidEmail("Invalid email format".into()));
        }

        Ok(())
    }

    pub fn value(&self) -> &str {
        &self.0
    }
}

impl From<Email> for String {
    fn from(email: Email) -> Self {
        email.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PhoneNumber(String);

impl PhoneNumber {
    pub fn new(phone: String) -> Result<Self, ValidationError> {
        Self::validate(&phone)?;
        Ok(Self(phone))
    }

    fn validate(phone: &str) -> Result<(), ValidationError> {
        let cleaned: String = phone
            .chars()
            .filter(|c| c.is_ascii_digit() || *c == '+')
            .collect();

        if cleaned.is_empty() {
            return Ok(());
        }

        if cleaned.starts_with('+') {
            if cleaned.len() < 8 || cleaned.len() > 16 {
                return Err(ValidationError::InvalidPhoneNumber(
                    "International phone number must be between 7 and 15 digits (plus '+')".into(),
                ));
            }
        } else if cleaned.len() < 7 || cleaned.len() > 15 {
            return Err(ValidationError::InvalidPhoneNumber(
                "Phone number must be between 7 and 15 digits".into(),
            ));
        }

        Ok(())
    }

    pub fn value(&self) -> &str {
        &self.0
    }
}

impl From<PhoneNumber> for String {
    fn from(phone: PhoneNumber) -> Self {
        phone.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_email_valid() {
        let valid_emails = vec![
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "test123@test-domain.com",
        ];

        for email in valid_emails {
            let result = Email::new(email.to_string());
            assert!(result.is_ok(), "Email '{}' should be valid", email);
        }
    }

    #[test]
    fn test_email_invalid() {
        let invalid_emails = vec![
            "",
            "notanemail",
            "missing@domain",
            "@nodomain.com",
            "no domain@.com",
            "spaces in@email.com",
        ];

        for email in invalid_emails {
            let result = Email::new(email.to_string());
            assert!(result.is_err(), "Email '{}' should be invalid", email);
        }
    }

    #[test]
    fn test_email_too_long() {
        let long_email = format!("{}@example.com", "a".repeat(250));
        let result = Email::new(long_email);
        assert!(result.is_err());
    }

    #[test]
    fn test_phone_number_valid() {
        let valid_phones = vec![
            "+1234567890",
            "+441234567890",
            "1234567890",
            "+12345678901234",
            "123-456-7890",
            "(123) 456-7890",
        ];

        for phone in valid_phones {
            let result = PhoneNumber::new(phone.to_string());
            assert!(result.is_ok(), "Phone '{}' should be valid", phone);
        }
    }

    #[test]
    fn test_phone_number_empty() {
        let result = PhoneNumber::new("".to_string());
        assert!(result.is_ok());
    }

    #[test]
    fn test_phone_number_too_short() {
        let result = PhoneNumber::new("12345".to_string());
        assert!(result.is_err());
    }

    #[test]
    fn test_phone_number_too_long() {
        let result = PhoneNumber::new("+12345678901234567".to_string());
        assert!(result.is_err());
    }
}
