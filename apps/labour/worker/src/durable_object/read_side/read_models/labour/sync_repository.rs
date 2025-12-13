use anyhow::{Context, Result, anyhow};
use fern_labour_event_sourcing_rs::{DecodedCursor, SyncRepositoryTrait};
use tracing::warn;
use uuid::Uuid;
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
                    updated_at TEXT NOT NULL
                )",
                None,
            )
            .map_err(|err| anyhow!("Failed to create labours table: {err}"))?;

        let _ = self
            .sql
            .exec("ALTER TABLE labours ADD COLUMN notes TEXT", None)
            .map_err(|err| warn!("Migration failed, it may have already run: {err}"));

        Ok(())
    }
}

impl SyncRepositoryTrait<LabourReadModel> for SqlLabourRepository {
    fn get(&self, limit: usize, _cursor: Option<DecodedCursor>) -> Result<Vec<LabourReadModel>> {
        let rows: Vec<LabourRow> = self
            .sql
            .exec(
                "SELECT * FROM labours LIMIT ?1",
                Some(vec![(limit as i32).into()]),
            )
            .context("Failed to execute labours query")?
            .to_array()
            .context("Failed to parse labour rows")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }

    fn get_by_id(&self, id: Uuid) -> Result<LabourReadModel> {
        let row: LabourRow = self
            .sql
            .exec(
                "SELECT * FROM labours WHERE labour_id=?1",
                Some(vec![id.to_string().into()]),
            )
            .context("Failed to execute labour query")?
            .one::<LabourRow>()
            .context("Failed to parse labour row")?;

        row.into_read_model()
    }

    fn delete(&self, id: Uuid) -> Result<()> {
        self.sql
            .exec(
                "DELETE FROM labours WHERE labour_id=?1",
                Some(vec![id.to_string().into()]),
            )
            .context("Failed to delete labour")?;

        Ok(())
    }

    fn upsert(&self, labour: &LabourReadModel) -> Result<()> {
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

        bindings.push(match row.notes {
            Some(notes) => notes.into(),
            None => worker::SqlStorageValue::Null,
        });

        bindings.push(row.created_at.into());
        bindings.push(row.updated_at.into());

        self.sql
            .exec(
                "INSERT INTO labours (
                    labour_id, birthing_person_id, current_phase, first_labour,
                    due_date, labour_name, start_time, end_time, notes,
                    created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)
                 ON CONFLICT(labour_id)
                 DO UPDATE SET
                    current_phase = ?3,
                    first_labour = ?4,
                    due_date = ?5,
                    labour_name = ?6,
                    start_time = ?7,
                    end_time = ?8,
                    notes = ?9,
                    updated_at = ?11",
                Some(bindings),
            )
            .context("Failed to upsert labour")?;

        Ok(())
    }

    fn overwrite(&self, labour: &LabourReadModel) -> Result<()> {
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

        bindings.push(match row.notes {
            Some(notes) => notes.into(),
            None => worker::SqlStorageValue::Null,
        });

        bindings.push(row.created_at.into());
        bindings.push(row.updated_at.into());

        self.sql
            .exec(
                "INSERT OR REPLACE INTO labours (
                    labour_id, birthing_person_id, current_phase, first_labour,
                    due_date, labour_name, start_time, end_time, notes,
                    created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)",
                Some(bindings),
            )
            .context("Failed to overwrite labour")?;

        Ok(())
    }
}
