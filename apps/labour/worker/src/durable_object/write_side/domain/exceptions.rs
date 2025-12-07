#[derive(Debug, Clone)]
pub enum LabourError {
    NotFound,
    InvalidStateTransition(String, String),
    ValidationError(String),
    InvalidCommand(String),
}

impl std::fmt::Display for LabourError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LabourError::NotFound => write!(f, "Labour not found"),
            LabourError::InvalidStateTransition(from_state, to_state) => {
                write!(
                    f,
                    "Cannot transition from state {from_state} to state {to_state}"
                )
            }
            LabourError::ValidationError(msg) => write!(f, "Validation error: {msg}"),
            LabourError::InvalidCommand(msg) => write!(f, "Invalid command: {msg}"),
        }
    }
}

impl std::error::Error for LabourError {}
