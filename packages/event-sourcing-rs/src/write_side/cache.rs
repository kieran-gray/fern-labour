use serde::{Serialize, de::DeserializeOwned};

#[derive(Debug, Clone)]
pub enum CacheError {
    WriteError(String),
    ReadError(String),
    DeleteError(String),
}

impl std::fmt::Display for CacheError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CacheError::WriteError(msg) => write!(f, "Write error: {msg}"),
            CacheError::ReadError(msg) => write!(f, "Read error: {msg}"),
            CacheError::DeleteError(msg) => write!(f, "Delete error: {msg}"),
        }
    }
}

impl std::error::Error for CacheError {}

pub trait CacheTrait {
    fn set_bytes(&self, key: String, value: Vec<u8>) -> Result<(), CacheError>;
    fn get_bytes(&self, key: String) -> Result<Option<Vec<u8>>, CacheError>;
    fn clear(&self, key: String) -> Result<(), CacheError>;
}

pub trait CacheExt: CacheTrait {
    fn set<T: Serialize>(&self, key: String, value: &T) -> Result<(), CacheError> {
        let bytes =
            serde_json::to_vec(value).map_err(|err| CacheError::WriteError(err.to_string()))?;
        self.set_bytes(key, bytes)
    }

    fn get<T: DeserializeOwned>(&self, key: String) -> Result<Option<T>, CacheError> {
        match self.get_bytes(key)? {
            Some(bytes) => {
                let val = serde_json::from_slice(&bytes)
                    .map_err(|err| CacheError::ReadError(err.to_string()))?;
                Ok(Some(val))
            }
            None => Ok(None),
        }
    }
}

impl<I: CacheTrait + ?Sized> CacheExt for I {}
