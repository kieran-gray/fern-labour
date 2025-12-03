use crate::domain::{DomainError, TokenClaims, UnverifiedJwt};

pub trait JwtParserTrait: Send + Sync {
    fn parse_unverified_jwt(&self, token: &str) -> Result<UnverifiedJwt, DomainError>;
    fn extract_issuer_from_unverified(&self, jwt: &UnverifiedJwt) -> Result<String, DomainError>;
    fn extract_claims(&self, jwt_payload: &serde_json::Value) -> Result<TokenClaims, DomainError>;
}
