use serde::{Deserialize, Serialize};

use crate::domain::jwks::jwk::Jwk;

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct JWKS {
    pub keys: Vec<Jwk>,
}

impl JWKS {
    pub fn get(&self, key_id: &str) -> Option<&Jwk> {
        self.keys
            .iter()
            .find(|jwk| jwk.kid.as_ref().map(|kid| kid == key_id).unwrap_or(false))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_test_jwk(kid: &str) -> Jwk {
        Jwk {
            kty: "RSA".to_string(),
            kid: Some(kid.to_string()),
            alg: Some("RS256".to_string()),
            n: "xGOr-H7A...".to_string(),
            e: "AQAB".to_string(),
        }
    }

    #[test]
    fn test_get_returns_key_when_kid_matches() {
        let jwk1 = create_test_jwk("key-1");
        let jwk2 = create_test_jwk("key-2");
        let jwks = JWKS {
            keys: vec![jwk1.clone(), jwk2.clone()],
        };

        let result = jwks.get("key-1");
        assert!(result.is_some());
        let key = result.unwrap();
        assert_eq!(key.kid.as_ref().unwrap(), "key-1");
        assert_eq!(key.n, jwk1.n);
    }

    #[test]
    fn test_get_returns_none_when_kid_not_found() {
        let jwk1 = create_test_jwk("key-1");
        let jwk2 = create_test_jwk("key-2");
        let jwks = JWKS {
            keys: vec![jwk1, jwk2],
        };

        let result = jwks.get("key-3");
        assert!(result.is_none());
    }

    #[test]
    fn test_get_ignores_keys_without_kid() {
        let jwk_with_kid = create_test_jwk("key-1");
        let jwk_without_kid = Jwk {
            kty: "RSA".to_string(),
            kid: None,
            alg: Some("RS256".to_string()),
            n: "xGOr-H7A...".to_string(),
            e: "AQAB".to_string(),
        };
        let jwks = JWKS {
            keys: vec![jwk_with_kid, jwk_without_kid],
        };

        let result = jwks.get("key-1");
        assert!(result.is_some());

        let result_none = jwks.get("");
        assert!(result_none.is_none());
    }

    #[test]
    fn test_get_is_case_sensitive() {
        let jwk = create_test_jwk("Key-1");
        let jwks = JWKS { keys: vec![jwk] };

        assert!(jwks.get("Key-1").is_some());

        assert!(jwks.get("key-1").is_none());
        assert!(jwks.get("KEY-1").is_none());
    }
}
