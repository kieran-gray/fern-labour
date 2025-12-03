#[derive(Debug)]
pub enum DomainError {
    InvalidJwt(String),
    UnsupportedAlgorithm(String),

    InvalidClaim(String),
    MissingClaim(String),
    InvalidClaims(Vec<String>),
    InvalidAudience {
        expected: String,
        actual: Vec<String>,
    },

    InvalidIdentity(String),

    InvalidIssuer(String),
    UnknownIssuer(String),
}

impl std::fmt::Display for DomainError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DomainError::InvalidJwt(msg) => write!(f, "Invalid JWT: {msg}"),
            DomainError::UnsupportedAlgorithm(alg) => write!(f, "Unsupported algorithm: {alg}"),
            DomainError::InvalidClaim(msg) => write!(f, "Invalid claim: {msg}"),
            DomainError::MissingClaim(claim) => write!(f, "Missing claim: {claim}"),
            DomainError::InvalidClaims(errs) => write!(f, "Invalid claims: {}", errs.join(", ")),
            DomainError::InvalidAudience { expected, actual } => {
                write!(
                    f,
                    "Invalid audience: expected '{}', got {:?}",
                    expected, actual
                )
            }
            DomainError::InvalidIdentity(msg) => write!(f, "Invalid identity: {msg}"),
            DomainError::InvalidIssuer(msg) => write!(f, "Invalid issuer: {msg}"),
            DomainError::UnknownIssuer(issuer) => write!(f, "Unknown issuer: {issuer}"),
        }
    }
}

impl std::error::Error for DomainError {}

#[derive(Debug, Clone)]
pub enum RepositoryError {
    FetchFailed(String),
    NotFound(String),
    DecodeError(String),
}

impl std::fmt::Display for RepositoryError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RepositoryError::FetchFailed(msg) => write!(f, "Save failed: {msg}"),
            RepositoryError::NotFound(msg) => write!(f, "Not found: {msg}"),
            RepositoryError::DecodeError(msg) => write!(f, "Error decoding: {msg}"),
        }
    }
}

impl std::error::Error for RepositoryError {}
