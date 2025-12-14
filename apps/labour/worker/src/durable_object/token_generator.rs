use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

pub trait SubscriptionTokenGenerator {
    fn generate(&self, user_id: &str, labour_id: &str) -> String;
    fn validate(&self, user_id: &str, labour_id: &str, token: &str) -> bool;
}

pub struct SplitMix64TokenGenerator {
    salt: String,
}

impl SplitMix64TokenGenerator {
    pub fn create(salt: String) -> Self {
        Self { salt }
    }

    fn splitmix64_finalizer(mut x: u64) -> u64 {
        x = x.wrapping_add(0x9e3779b97f4a7c15);
        x = (x ^ (x >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        x = (x ^ (x >> 27)).wrapping_mul(0x94d049bb133111eb);
        x ^ (x >> 31)
    }

    fn hash_to_u64(input: &str) -> u64 {
        let mut hasher = DefaultHasher::new();
        input.hash(&mut hasher);
        hasher.finish()
    }

    fn generate_token(&self, user_id: &str, labour_id: &str) -> String {
        let combined = format!("{}{}{}", user_id, labour_id, self.salt);

        let hash = Self::hash_to_u64(&combined);

        let finalized = Self::splitmix64_finalizer(hash);

        let token = finalized % 100000;
        format!("{:05}", token)
    }
}

impl SubscriptionTokenGenerator for SplitMix64TokenGenerator {
    fn generate(&self, user_id: &str, labour_id: &str) -> String {
        self.generate_token(user_id, labour_id)
    }

    fn validate(&self, user_id: &str, labour_id: &str, token: &str) -> bool {
        let expected_token = self.generate_token(user_id, labour_id);
        expected_token == token
    }
}
