use std::collections::HashMap;

use crate::{
    application::exceptions::AppError,
    domain::{AuthenticatedPrincipal, TokenClaims},
};

pub trait IdentityExtractionServiceTrait: Send + Sync {
    fn extract_principal(
        &self,
        claims: &TokenClaims,
        issuer_name: &str,
    ) -> Result<AuthenticatedPrincipal, AppError>;
}

pub struct IdentityExtractionService {
    extractors: HashMap<String, Box<dyn ClaimsExtractor>>,
}

impl IdentityExtractionService {
    pub fn create(extractors: HashMap<String, Box<dyn ClaimsExtractor>>) -> Self {
        Self { extractors }
    }
}

impl IdentityExtractionService {
    fn get_extractor(&self, issuer: &str) -> Option<&dyn ClaimsExtractor> {
        self.extractors.get(issuer).map(|b| b.as_ref())
    }
}

impl IdentityExtractionServiceTrait for IdentityExtractionService {
    fn extract_principal(
        &self,
        claims: &TokenClaims,
        issuer_name: &str,
    ) -> Result<AuthenticatedPrincipal, AppError> {
        let extractor = self
            .get_extractor(issuer_name)
            .ok_or(AppError::InternalError(format!(
                "No extractor for {}",
                issuer_name
            )))?;

        AuthenticatedPrincipal::new(
            claims.subject.to_string(),
            claims.issuer.to_string(),
            extractor.extract_email(&claims.custom_claims),
            extractor.extract_email_verified(&claims.custom_claims),
            extractor.extract_name(&claims.custom_claims),
            claims.custom_claims.clone(),
        )
        .map_err(|e| AppError::InternalError(e.to_string()))
    }
}

pub trait ClaimsExtractor: Send + Sync {
    fn extract_email(&self, claims: &serde_json::Value) -> Option<String>;
    fn extract_email_verified(&self, claims: &serde_json::Value) -> Option<bool>;
    fn extract_name(&self, claims: &serde_json::Value) -> Option<String>;
    fn extract_roles(&self, claims: &serde_json::Value) -> Vec<String>;
}
