use thiserror::Error;
use tracing::error;

#[derive(Error, Debug)]
pub enum InfrastructureError {
    #[error("Database Row To Domain Conversion error: {0}")]
    DatabaseRowToDomainConversionError(String),
}
