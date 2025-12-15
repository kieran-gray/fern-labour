#[derive(Debug, Clone)]
pub enum ValidationError {
    InvalidEmail(String),
    InvalidFirstName(String),
    InvalidLastName(String),
    InvalidPhoneNumber(String),
    InvalidUserId(String),
}

impl std::fmt::Display for ValidationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ValidationError::InvalidEmail(msg) => write!(f, "Invalid email: {msg}"),
            ValidationError::InvalidFirstName(msg) => write!(f, "Invalid first name: {msg}"),
            ValidationError::InvalidLastName(msg) => write!(f, "Invalid last name: {msg}"),
            ValidationError::InvalidPhoneNumber(msg) => write!(f, "Invalid phone number: {msg}"),
            ValidationError::InvalidUserId(msg) => write!(f, "Invalid user ID: {msg}"),
        }
    }
}

impl std::error::Error for ValidationError {}

#[derive(Debug, Clone)]
pub enum RepositoryError {
    SaveFailed(String),
    NotFound(String),
    DatabaseError(String),
    AlreadyExists(String),
}

impl std::fmt::Display for RepositoryError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RepositoryError::SaveFailed(msg) => write!(f, "Save failed: {msg}"),
            RepositoryError::NotFound(msg) => write!(f, "Not found: {msg}"),
            RepositoryError::DatabaseError(msg) => write!(f, "Database error: {msg}"),
            RepositoryError::AlreadyExists(msg) => write!(f, "Already exists: {msg}"),
        }
    }
}

impl std::error::Error for RepositoryError {}
