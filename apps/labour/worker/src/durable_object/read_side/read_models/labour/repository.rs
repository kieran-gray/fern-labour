use anyhow::{Context, Result};
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::SingleItemRepositoryTrait;
use worker::SqlStorage;

use super::read_model::{LabourReadModel, LabourRow};

pub struct SqlLabourRepository {
    sql: SqlStorage,
}

impl SqlLabourRepository {
    pub fn create(sql: SqlStorage) -> Self {
        Self { sql }
    }

    pub fn init_schema(&self) -> Result<()> {
        self.sql
            .exec(
                "CREATE TABLE IF NOT EXISTS labours (
                    labour_id TEXT PRIMARY KEY,
                    birthing_person_id TEXT NOT NULL,
                    current_phase TEXT NOT NULL,
                    first_labour TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    labour_name TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                )",
                None,
            )
            .context("Failed to create labours table")?;

        Ok(())
    }
}

#[async_trait(?Send)]
impl SingleItemRepositoryTrait<LabourReadModel> for SqlLabourRepository {
    async fn get(&self) -> Result<LabourReadModel> {
        let row: LabourRow = self
            .sql
            .exec("SELECT * FROM labours", None)
            .context("Failed to execute labours query")?
            .one::<LabourRow>()
            .context("Failed to parse labour row")?;

        row.into_read_model()
    }

    async fn delete(&self) -> Result<()> {
        self.sql
            .exec("DELETE FROM labours", None)
            .context("Failed to delete labour")?;

        Ok(())
    }

    async fn overwrite(&self, labour: &LabourReadModel) -> Result<()> {
        let row = LabourRow::from_read_model(labour).context("Failed to convert labour to row")?;

        let mut bindings = vec![
            row.labour_id.into(),
            row.birthing_person_id.into(),
            row.current_phase.into(),
            row.first_labour.into(),
            row.due_date.into(),
        ];

        bindings.push(match row.labour_name {
            Some(name) => name.into(),
            None => worker::SqlStorageValue::Null,
        });

        bindings.push(match row.start_time {
            Some(time) => time.into(),
            None => worker::SqlStorageValue::Null,
        });

        bindings.push(match row.end_time {
            Some(time) => time.into(),
            None => worker::SqlStorageValue::Null,
        });

        bindings.push(row.created_at.into());
        bindings.push(row.updated_at.into());

        self.sql
            .exec(
                "INSERT OR REPLACE INTO labours (
                    labour_id, birthing_person_id, current_phase, first_labour,
                    due_date, labour_name, start_time, end_time,
                    created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10)",
                Some(bindings),
            )
            .context("Failed to overwrite labour")?;

        Ok(())
    }
}
