use serde::{Deserialize, Serialize};
use std::fmt::{self, Display};

use crate::value_objects::NotificationChannel;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct EmailAddress(String);

impl EmailAddress {
    pub fn new(email: impl Into<String>) -> Result<Self, ValidationError> {
        let email = email.into();
        Self::validate(&email)?;
        Ok(Self(email))
    }

    fn validate(email: &str) -> Result<(), ValidationError> {
        if email.is_empty() {
            return Err(ValidationError::EmptyEmail);
        }

        let parts: Vec<&str> = email.split('@').collect();
        if parts.len() != 2 {
            return Err(ValidationError::InvalidEmailFormat(
                "Email must contain exactly one @ symbol".to_string(),
            ));
        }

        let local = parts[0];
        let domain = parts[1];

        if local.is_empty() {
            return Err(ValidationError::InvalidEmailFormat(
                "Email local part cannot be empty".to_string(),
            ));
        }

        if domain.is_empty() || !domain.contains('.') {
            return Err(ValidationError::InvalidEmailFormat(
                "Email domain must contain at least one dot".to_string(),
            ));
        }

        if email.contains(char::is_whitespace) {
            return Err(ValidationError::InvalidEmailFormat(
                "Email cannot contain whitespace".to_string(),
            ));
        }

        Ok(())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }

    pub fn into_inner(self) -> String {
        self.0
    }
}

impl Display for EmailAddress {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl TryFrom<String> for EmailAddress {
    type Error = ValidationError;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl TryFrom<&str> for EmailAddress {
    type Error = ValidationError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        Self::new(value.to_string())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct PhoneNumber(String);

impl PhoneNumber {
    pub fn new(phone: impl Into<String>) -> Result<Self, ValidationError> {
        let phone = phone.into();
        Self::validate(&phone)?;
        Ok(Self(phone))
    }

    fn validate(phone: &str) -> Result<(), ValidationError> {
        if phone.is_empty() {
            return Err(ValidationError::EmptyPhoneNumber);
        }

        if !phone.starts_with('+') {
            return Err(ValidationError::InvalidPhoneFormat(
                "Phone number must start with + (E.164 format)".to_string(),
            ));
        }

        let digits = &phone[1..];

        if digits.is_empty() {
            return Err(ValidationError::InvalidPhoneFormat(
                "Phone number must contain digits after +".to_string(),
            ));
        }

        if !digits.chars().all(|c| c.is_ascii_digit()) {
            return Err(ValidationError::InvalidPhoneFormat(
                "Phone number must contain only digits after +".to_string(),
            ));
        }

        let digit_count = digits.len();
        if !(1..=15).contains(&digit_count) {
            return Err(ValidationError::InvalidPhoneFormat(format!(
                "Phone number must have 1-15 digits, got {}",
                digit_count
            )));
        }

        Ok(())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }

    pub fn into_inner(self) -> String {
        self.0
    }
}

impl Display for PhoneNumber {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl TryFrom<String> for PhoneNumber {
    type Error = ValidationError;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl TryFrom<&str> for PhoneNumber {
    type Error = ValidationError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        Self::new(value.to_string())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct WhatsAppId(String);

impl WhatsAppId {
    pub fn new(whatsapp_id: impl Into<String>) -> Result<Self, ValidationError> {
        let whatsapp_id = whatsapp_id.into();

        PhoneNumber::validate(&whatsapp_id)?;
        Ok(Self(whatsapp_id))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }

    pub fn into_inner(self) -> String {
        self.0
    }
}

impl Display for WhatsAppId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl TryFrom<String> for WhatsAppId {
    type Error = ValidationError;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl TryFrom<&str> for WhatsAppId {
    type Error = ValidationError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        Self::new(value.to_string())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(tag = "type", content = "value")]
pub enum NotificationDestination {
    Email(EmailAddress),
    PhoneNumber(PhoneNumber),
    WhatsAppId(WhatsAppId),
}

impl NotificationDestination {
    pub fn from_string_and_channel(
        destination: String,
        channel: &crate::value_objects::NotificationChannel,
    ) -> Result<Self, ValidationError> {
        use crate::value_objects::NotificationChannel;

        match channel {
            NotificationChannel::EMAIL => Ok(NotificationDestination::Email(EmailAddress::new(
                destination,
            )?)),
            NotificationChannel::SMS => Ok(NotificationDestination::PhoneNumber(PhoneNumber::new(
                destination,
            )?)),
            NotificationChannel::WHATSAPP => Ok(NotificationDestination::WhatsAppId(
                WhatsAppId::new(destination)?,
            )),
        }
    }

    pub fn as_str(&self) -> &str {
        match self {
            NotificationDestination::Email(email) => email.as_str(),
            NotificationDestination::PhoneNumber(phone) => phone.as_str(),
            NotificationDestination::WhatsAppId(whatsapp) => whatsapp.as_str(),
        }
    }

    pub fn channel(&self) -> crate::value_objects::NotificationChannel {
        use crate::value_objects::NotificationChannel;

        match self {
            NotificationDestination::Email(_) => NotificationChannel::EMAIL,
            NotificationDestination::PhoneNumber(_) => NotificationChannel::SMS,
            NotificationDestination::WhatsAppId(_) => NotificationChannel::WHATSAPP,
        }
    }

    pub fn matches_channel(&self, channel: &NotificationChannel) -> bool {
        &self.channel() == channel
    }

    pub fn into_inner(self) -> String {
        match self {
            NotificationDestination::Email(email) => email.into_inner(),
            NotificationDestination::PhoneNumber(phone) => phone.into_inner(),
            NotificationDestination::WhatsAppId(whatsapp) => whatsapp.into_inner(),
        }
    }
}

impl Display for NotificationDestination {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ValidationError {
    EmptyEmail,
    InvalidEmailFormat(String),
    EmptyPhoneNumber,
    InvalidPhoneFormat(String),
}

impl Display for ValidationError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ValidationError::EmptyEmail => write!(f, "Email address cannot be empty"),
            ValidationError::InvalidEmailFormat(msg) => write!(f, "Invalid email format: {}", msg),
            ValidationError::EmptyPhoneNumber => write!(f, "Phone number cannot be empty"),
            ValidationError::InvalidPhoneFormat(msg) => write!(f, "Invalid phone format: {}", msg),
        }
    }
}

impl std::error::Error for ValidationError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_email_addresses() {
        assert!(EmailAddress::new("user@example.com").is_ok());
        assert!(EmailAddress::new("test.user@domain.co.uk").is_ok());
        assert!(EmailAddress::new("user+tag@example.com").is_ok());
    }

    #[test]
    fn test_invalid_email_addresses() {
        assert!(EmailAddress::new("").is_err());
        assert!(EmailAddress::new("notanemail").is_err());
        assert!(EmailAddress::new("@example.com").is_err());
        assert!(EmailAddress::new("user@").is_err());
        assert!(EmailAddress::new("user @example.com").is_err());
        assert!(EmailAddress::new("user@nodomain").is_err());
    }

    #[test]
    fn test_valid_phone_numbers() {
        assert!(PhoneNumber::new("+1234567890").is_ok());
        assert!(PhoneNumber::new("+442012345678").is_ok());
        assert!(PhoneNumber::new("+12025551234").is_ok());
        assert!(PhoneNumber::new("+1").is_ok());
        assert!(PhoneNumber::new("+123456789012345").is_ok());
    }

    #[test]
    fn test_invalid_phone_numbers() {
        assert!(PhoneNumber::new("").is_err());
        assert!(PhoneNumber::new("1234567890").is_err());
        assert!(PhoneNumber::new("+").is_err());
        assert!(PhoneNumber::new("+123-456-7890").is_err());
        assert!(PhoneNumber::new("+123 456 7890").is_err());
        assert!(PhoneNumber::new("+1234567890123456").is_err());
    }

    #[test]
    fn test_valid_whatsapp_ids() {
        assert!(WhatsAppId::new("+1234567890").is_ok());
        assert!(WhatsAppId::new("+442012345678").is_ok());
    }

    #[test]
    fn test_invalid_whatsapp_ids() {
        assert!(WhatsAppId::new("").is_err());
        assert!(WhatsAppId::new("1234567890").is_err());
    }

    #[test]
    fn test_notification_destination_from_string_and_channel() {
        use crate::value_objects::NotificationChannel;

        let email_dest = NotificationDestination::from_string_and_channel(
            "test@example.com".to_string(),
            &NotificationChannel::EMAIL,
        );
        assert!(email_dest.is_ok());
        assert!(matches!(
            email_dest.unwrap(),
            NotificationDestination::Email(_)
        ));

        let sms_dest = NotificationDestination::from_string_and_channel(
            "+1234567890".to_string(),
            &NotificationChannel::SMS,
        );
        assert!(sms_dest.is_ok());
        assert!(matches!(
            sms_dest.unwrap(),
            NotificationDestination::PhoneNumber(_)
        ));

        let whatsapp_dest = NotificationDestination::from_string_and_channel(
            "+1234567890".to_string(),
            &NotificationChannel::WHATSAPP,
        );
        assert!(whatsapp_dest.is_ok());
        assert!(matches!(
            whatsapp_dest.unwrap(),
            NotificationDestination::WhatsAppId(_)
        ));
    }

    #[test]
    fn test_notification_destination_validation() {
        use crate::value_objects::NotificationChannel;

        let result = NotificationDestination::from_string_and_channel(
            "notanemail".to_string(),
            &NotificationChannel::EMAIL,
        );
        assert!(result.is_err());

        let result = NotificationDestination::from_string_and_channel(
            "1234567890".to_string(),
            &NotificationChannel::SMS,
        );
        assert!(result.is_err());
    }

    #[test]
    fn test_notification_destination_matches_channel() {
        use crate::value_objects::NotificationChannel;

        let email = NotificationDestination::Email(EmailAddress::new("test@example.com").unwrap());
        assert!(email.matches_channel(&NotificationChannel::EMAIL));
        assert!(!email.matches_channel(&NotificationChannel::SMS));

        let phone = NotificationDestination::PhoneNumber(PhoneNumber::new("+1234567890").unwrap());
        assert!(phone.matches_channel(&NotificationChannel::SMS));
        assert!(!phone.matches_channel(&NotificationChannel::EMAIL));
    }

    #[test]
    fn test_notification_destination_as_str() {
        let email = NotificationDestination::Email(EmailAddress::new("test@example.com").unwrap());
        assert_eq!(email.as_str(), "test@example.com");

        let phone = NotificationDestination::PhoneNumber(PhoneNumber::new("+1234567890").unwrap());
        assert_eq!(phone.as_str(), "+1234567890");
    }
}
