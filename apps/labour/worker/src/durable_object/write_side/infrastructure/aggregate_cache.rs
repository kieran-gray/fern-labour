use fern_labour_event_sourcing_rs::{CacheError, CacheTrait};
use tracing::warn;
use worker::{SqlStorage, SqlStorageValue};

pub struct SqlCache {
    sql: SqlStorage,
}

impl SqlCache {
    pub fn new(sql: SqlStorage) -> Self {
        Self { sql }
    }

    pub fn init_schema(&self) -> Result<(), CacheError> {
        self.sql
            .exec(
                "CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value BLOB NOT NULL
                )",
                None,
            )
            .map_err(|e| CacheError::WriteError(e.to_string()))?;
        Ok(())
    }
}

impl CacheTrait for SqlCache {
    fn set_bytes(&self, key: String, value: Vec<u8>) -> Result<(), CacheError> {
        self.sql
            .exec(
                "INSERT OR REPLACE INTO cache (key, value) VALUES (?1, ?2)",
                Some(vec![
                    SqlStorageValue::String(key.clone()),
                    SqlStorageValue::Blob(value),
                ]),
            )
            .map_err(|e| {
                warn!(key = %key, error = %e, "SqlCache: Failed to write to cache");
                CacheError::WriteError(e.to_string())
            })?;
        Ok(())
    }

    fn get_bytes(&self, key: String) -> Result<Option<Vec<u8>>, CacheError> {
        let cursor = self
            .sql
            .exec(
                "SELECT value FROM cache WHERE key = ?1",
                Some(vec![SqlStorageValue::String(key.clone())]),
            )
            .map_err(|e| {
                warn!(key = %key, error = %e, "SqlCache: SQL exec failed");
                CacheError::ReadError(format!("SQL exec failed: {}", e))
            })?;

        let mut results = cursor.raw();

        match results.next() {
            Some(Ok(row)) => match row.first() {
                Some(SqlStorageValue::Blob(bytes)) => Ok(Some(bytes.clone())),
                Some(other) => {
                    warn!(key = %key, value_type = ?other, "SqlCache: Unexpected value type");
                    Err(CacheError::ReadError(format!(
                        "Expected Blob, got {:?}",
                        other
                    )))
                }
                None => {
                    warn!(key = %key, "SqlCache: Row has no columns");
                    Err(CacheError::ReadError("Row has no columns".to_string()))
                }
            },
            Some(Err(e)) => {
                warn!(key = %key, error = %e, "SqlCache: Error reading row");
                Err(CacheError::ReadError(format!("Error reading row: {}", e)))
            }
            None => Ok(None),
        }
    }

    fn clear(&self, key: String) -> Result<(), CacheError> {
        self.sql
            .exec(
                "DELETE FROM cache WHERE key = ?1",
                Some(vec![SqlStorageValue::String(key.clone())]),
            )
            .map_err(|e| {
                warn!(key = %key, error = %e, "SqlCache: Failed to clear cache");
                CacheError::DeleteError(e.to_string())
            })?;
        Ok(())
    }
}
