use crate::application::services::identity_extraction_service::ClaimsExtractor;

pub struct CloudflareClaimsExtractor;
impl ClaimsExtractor for CloudflareClaimsExtractor {
    fn extract_email(&self, claims: &serde_json::Value) -> Option<String> {
        claims.get("email")?.as_str().map(String::from)
    }

    fn extract_email_verified(&self, claims: &serde_json::Value) -> Option<bool> {
        claims.get("email_verified").and_then(|v| v.as_bool())
    }

    fn extract_name(&self, claims: &serde_json::Value) -> Option<String> {
        claims
            .get("name")
            .or_else(|| claims.get("common_name"))
            .and_then(|v| v.as_str())
            .map(String::from)
    }

    fn extract_roles(&self, claims: &serde_json::Value) -> Vec<String> {
        claims
            .get("groups")
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str())
                    .map(String::from)
                    .collect()
            })
            .unwrap_or_default()
    }
}
