use crate::durable_object::write_side::domain::LabourError;

#[derive(Debug)]
pub enum AppError {
    Domain(LabourError),
    Unauthorised(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AppError::Domain(e) => write!(f, "{}", e),
            AppError::Unauthorised(msg) => write!(f, "{}", msg),
        }
    }
}

impl std::error::Error for AppError {}

impl From<AppError> for worker::Response {
    fn from(error: AppError) -> Self {
        let (msg, status) = match &error {
            AppError::Domain(err) => (err.to_string(), 400),
            AppError::Unauthorised(err) => (err.clone(), 403),
        };
        worker::Response::error(&msg, status).unwrap()
    }
}

pub trait IntoWorkerResponse {
    fn into_response(self) -> worker::Response;
}

impl IntoWorkerResponse for anyhow::Error {
    fn into_response(self) -> worker::Response {
        if let Some(app_err) = self.downcast_ref::<AppError>() {
            return worker::Response::from(app_err.clone());
        }

        worker::Response::error(format!("{:#}", self), 500).unwrap()
    }
}

impl Clone for AppError {
    fn clone(&self) -> Self {
        match self {
            AppError::Domain(e) => AppError::Domain(e.clone()),
            AppError::Unauthorised(msg) => AppError::Unauthorised(msg.clone()),
        }
    }
}
