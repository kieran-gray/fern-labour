use anyhow::Result;
use serde::{Deserialize, Serialize};
use strum::EnumString;
use worker::SqlStorage;

#[derive(Debug, Clone, Deserialize, Serialize, EnumString, PartialEq, Hash, Eq)]
pub enum ProcessingStatus {
    #[strum(serialize = "PROCESSING")]
    PROCESSING,
    #[strum(serialize = "PROCESSED")]
    PROCESSED,
    #[strum(serialize = "FAILED")]
    FAILED,
}

impl std::fmt::Display for ProcessingStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ProcessingStatus::PROCESSING => write!(f, "PROCESSING"),
            ProcessingStatus::PROCESSED => write!(f, "PROCESSED"),
            ProcessingStatus::FAILED => write!(f, "FAILED"),
        }
    }
}

#[derive(Debug, Clone, Deserialize)]
pub struct ProcessingEntry {
    pub event_sequence: i64,
    pub status: ProcessingStatus,
    pub retry_count: i64,
    pub last_error: Option<String>,
}

#[derive(Deserialize)]
struct LastProcessedRow {
    last_seq: Option<i64>,
}

#[derive(Clone)]
pub struct PolicyApplicationTracker {
    sql: SqlStorage,
}

impl PolicyApplicationTracker {
    pub fn create(sql: SqlStorage) -> Self {
        Self { sql }
    }

    pub fn init_schema(&self) -> Result<()> {
        self.sql.exec(
            "CREATE TABLE IF NOT EXISTS event_processing (
                event_sequence INTEGER PRIMARY KEY,
                status TEXT DEFAULT 'PROCESSING' NOT NULL,
                retry_count INTEGER DEFAULT 0,
                last_error TEXT,
                FOREIGN KEY (event_sequence) REFERENCES events(sequence)
            )",
            None,
        )?;
        Ok(())
    }

    pub fn get_last_processed_sequence(&self) -> Result<Option<i64>> {
        let row: LastProcessedRow = self
            .sql
            .exec(
                "SELECT MAX(event_sequence) as last_seq FROM event_processing WHERE status = 'PROCESSED'",
                None,
            )?
            .one()?;

        Ok(row.last_seq)
    }

    pub fn get_or_create_entry(&self, sequence: i64) -> Result<ProcessingEntry> {
        let results: Vec<ProcessingEntry> = self
            .sql
            .exec(
                "SELECT * FROM event_processing WHERE event_sequence = ?1",
                Some(vec![sequence.into()]),
            )?
            .to_array()?;

        if let Some(entry) = results.into_iter().next() {
            return Ok(entry);
        }

        self.sql.exec(
            "INSERT INTO event_processing (event_sequence) VALUES (?1)",
            Some(vec![sequence.into()]),
        )?;

        Ok(ProcessingEntry {
            event_sequence: sequence,
            status: ProcessingStatus::PROCESSING,
            retry_count: 0,
            last_error: None,
        })
    }

    pub fn mark_completed(&self, sequence: i64) -> Result<()> {
        self.sql.exec(
            "UPDATE event_processing
             SET status = 'PROCESSED'
             WHERE event_sequence = ?1",
            Some(vec![sequence.into()]),
        )?;
        Ok(())
    }

    pub fn increment_retry(&self, sequence: i64, error: &str) -> Result<()> {
        self.sql.exec(
            "UPDATE event_processing 
             SET retry_count = retry_count + 1,
                 last_error = ?2
             WHERE event_sequence = ?1",
            Some(vec![sequence.into(), error.into()]),
        )?;
        Ok(())
    }
}
