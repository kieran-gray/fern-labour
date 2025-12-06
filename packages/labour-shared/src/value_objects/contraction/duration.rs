use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug)]
pub enum DurationError {
    ContractionStartTimeAfterEndTime,
}

impl std::fmt::Display for DurationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DurationError::ContractionStartTimeAfterEndTime => {
                write!(f, "Contraction start time cannot be after end time")
            }
        }
    }
}

impl std::error::Error for DurationError {}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub struct Duration {
    start_time: DateTime<Utc>,
    end_time: DateTime<Utc>,
}

impl Duration {
    pub fn create(
        start_time: DateTime<Utc>,
        end_time: DateTime<Utc>,
    ) -> Result<Self, DurationError> {
        if start_time > end_time {
            return Err(DurationError::ContractionStartTimeAfterEndTime);
        }

        Ok(Self {
            start_time,
            end_time,
        })
    }

    pub fn start_time(&self) -> &DateTime<Utc> {
        &self.start_time
    }

    pub fn end_time(&self) -> &DateTime<Utc> {
        &self.end_time
    }

    pub fn duration_seconds(&self) -> f64 {
        (self.end_time - self.start_time).num_milliseconds() as f64 / 1000.0
    }

    pub fn duration_minutes(&self) -> f64 {
        self.duration_seconds() / 60.0
    }
}

impl fmt::Display for Duration {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let total_seconds = self.duration_seconds() as i64;
        let minutes = total_seconds / 60;
        let seconds = total_seconds % 60;
        write!(f, "{}m {}s", minutes, seconds)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::TimeZone;

    #[test]
    fn test_create_valid_duration() {
        let start = Utc.with_ymd_and_hms(2024, 1, 1, 12, 0, 0).unwrap();
        let end = Utc.with_ymd_and_hms(2024, 1, 1, 12, 1, 30).unwrap();

        let duration = Duration::create(start, end).unwrap();
        assert_eq!(duration.duration_seconds(), 90.0);
        assert_eq!(duration.duration_minutes(), 1.5);
    }

    #[test]
    fn test_create_temp_duration() {
        let time = Utc.with_ymd_and_hms(2024, 1, 1, 12, 0, 0).unwrap();

        let duration = Duration::create(time, time).unwrap();
        assert_eq!(duration.duration_seconds(), 0.0);
    }

    #[test]
    fn test_create_invalid_duration() {
        let start = Utc.with_ymd_and_hms(2024, 1, 1, 12, 1, 0).unwrap();
        let end = Utc.with_ymd_and_hms(2024, 1, 1, 12, 0, 0).unwrap();

        let result = Duration::create(start, end);
        assert!(result.is_err());
    }

    #[test]
    fn test_display() {
        let start = Utc.with_ymd_and_hms(2024, 1, 1, 12, 0, 0).unwrap();
        let end = Utc.with_ymd_and_hms(2024, 1, 1, 12, 2, 35).unwrap();

        let duration = Duration::create(start, end).unwrap();
        assert_eq!(duration.to_string(), "2m 35s");
    }
}
