use crate::application::services::identity_extraction_service::ClaimsExtractor;

pub struct ClerkClaimsExtractor;

impl ClaimsExtractor for ClerkClaimsExtractor {
    fn extract_email(&self, claims: &serde_json::Value) -> Option<String> {
        claims
            .get("email_address")
            .and_then(|v| v.as_str())
            .map(String::from)
    }

    fn extract_email_verified(&self, claims: &serde_json::Value) -> Option<bool> {
        if claims.get("email_address").is_some() {
            Some(true)
        } else {
            None
        }
    }

    fn extract_phone_number(&self, claims: &serde_json::Value) -> Option<String> {
        claims
            .get("phone_number")
            .and_then(|v| v.as_str())
            .map(String::from)
    }

    fn extract_phone_number_verified(&self, claims: &serde_json::Value) -> Option<String> {
        if claims.get("phone_number").is_some() {
            Some("true".to_string())
        } else {
            None
        }
    }

    fn extract_first_name(&self, claims: &serde_json::Value) -> Option<String> {
        claims
            .get("first_name")
            .and_then(|v| v.as_str())
            .map(String::from)
    }

    fn extract_last_name(&self, claims: &serde_json::Value) -> Option<String> {
        claims
            .get("last_name")
            .and_then(|v| v.as_str())
            .map(String::from)
    }

    fn extract_name(&self, claims: &serde_json::Value) -> Option<String> {
        let first = claims.get("first_name")?.as_str()?;
        let last = claims.get("last_name").and_then(|v| v.as_str());

        match last {
            Some(last_name) => Some(format!("{} {}", first, last_name)),
            None => Some(first.to_string()),
        }
    }

    fn extract_roles(&self, claims: &serde_json::Value) -> Vec<String> {
        claims
            .get("public_metadata")
            .and_then(|m| m.get("roles"))
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str())
                    .map(String::from)
                    .collect()
            })
            .or_else(|| {
                claims
                    .get("org_role")
                    .and_then(|v| v.as_str())
                    .map(|role| vec![role.to_string()])
            })
            .unwrap_or_default()
    }
}
