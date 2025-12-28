use anyhow::{Context, Result, anyhow};
use fern_labour_event_sourcing_rs::{DecodedCursor, SyncRepositoryTrait};
use uuid::Uuid;
use worker::SqlStorage;

use super::read_model::{LabourUpdateReadModel, LabourUpdateRow};

pub struct SqlLabourUpdateRepository {
    sql: SqlStorage,
}

impl SqlLabourUpdateRepository {
    pub fn create(sql: SqlStorage) -> Self {
        Self { sql }
    }

    pub fn init_schema(&self) -> Result<()> {
        self.sql
            .exec(
                "CREATE TABLE IF NOT EXISTS labour_updates (
                    labour_update_id TEXT PRIMARY KEY,
                    labour_id TEXT NOT NULL,
                    labour_update_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    edited TEXT NOT NULL,
                    application_generated TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )",
                None,
            )
            .map_err(|err| anyhow!("Failed to create labour_updates table: {err}"))?;

        self.sql
            .exec(
                "CREATE INDEX IF NOT EXISTS idx_labour_updates_created_at
                 ON labour_updates(created_at DESC)",
                None,
            )
            .context("Failed to create created_at index")?;

        Ok(())
    }

    pub fn get_all(&self) -> Result<Vec<LabourUpdateReadModel>> {
        let rows: Vec<LabourUpdateRow> = self
            .sql
            .exec("SELECT * FROM labour_updates ORDER BY created_at ASC", None)
            .context("Failed to execute labour_updates query")?
            .to_array()
            .context("Failed to fetch labour_updates")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }

    pub fn get_by_labour_id(&self, labour_id: Uuid) -> Result<Vec<LabourUpdateReadModel>> {
        let rows: Vec<LabourUpdateRow> = self
            .sql
            .exec(
                "SELECT * FROM labour_updates WHERE labour_id = ?1 ORDER BY created_at ASC",
                Some(vec![labour_id.to_string().into()]),
            )
            .context("Failed to execute labour_updates query")?
            .to_array()
            .context("Failed to fetch labour_updates")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }
}

impl SyncRepositoryTrait<LabourUpdateReadModel> for SqlLabourUpdateRepository {
    fn get_by_id(&self, labour_update_id: Uuid) -> Result<LabourUpdateReadModel> {
        let rows: Vec<LabourUpdateRow> = self
            .sql
            .exec(
                "SELECT * FROM labour_updates WHERE labour_update_id = ?1",
                Some(vec![labour_update_id.to_string().into()]),
            )
            .context("Failed to execute labour_update query")?
            .to_array()
            .context("Failed to fetch labour_update")?;

        match rows.into_iter().next() {
            Some(row) => row.into_read_model(),
            None => Err(anyhow::anyhow!("LabourUpdate not found")),
        }
    }

    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<LabourUpdateReadModel>> {
        let mut query = "SELECT * FROM labour_updates".to_string();
        let mut bindings = vec![];

        if let Some(cur) = cursor {
            query.push_str(" WHERE created_at < ?1 OR (created_at = ?1 AND labour_update_id < ?2)");
            bindings.push(cur.last_updated_at.to_rfc3339().into());
            bindings.push(cur.last_id.to_string().into());
        }

        let limit_param_index = bindings.len() + 1;
        query.push_str(&format!(
            " ORDER BY created_at DESC, labour_update_id DESC LIMIT ?{}",
            limit_param_index
        ));

        let plus_one_limit = limit + 1;
        bindings.push((plus_one_limit as f64).into());

        let rows: Vec<LabourUpdateRow> = self
            .sql
            .exec(&query, Some(bindings))
            .context("Failed to execute labour_updates query")?
            .to_array()
            .context("Failed to fetch labour_updates")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }

    fn upsert(&self, labour_update: &LabourUpdateReadModel) -> Result<()> {
        let row = LabourUpdateRow::from_read_model(labour_update)
            .context("Failed to convert labour_update to row")?;

        let bindings = vec![
            row.labour_update_id.into(),
            row.labour_id.into(),
            row.labour_update_type.into(),
            row.message.into(),
            row.edited.into(),
            row.application_generated.into(),
            row.created_at.into(),
            row.updated_at.into(),
        ];

        self.sql
            .exec(
                "INSERT INTO labour_updates (
                    labour_update_id, labour_id, labour_update_type, message,
                    edited, application_generated, created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)
                 ON CONFLICT(labour_update_id)
                 DO UPDATE SET
                    labour_update_type = ?3,
                    message = ?4,
                    edited = ?5,
                    application_generated = ?6,
                    updated_at = ?8",
                Some(bindings),
            )
            .context("Failed to upsert labour_update")?;

        Ok(())
    }

    fn delete(&self, labour_update_id: Uuid) -> Result<()> {
        self.sql
            .exec(
                "DELETE FROM labour_updates WHERE labour_update_id = ?1",
                Some(vec![labour_update_id.to_string().into()]),
            )
            .context("Failed to delete labour_update")?;

        Ok(())
    }

    fn overwrite(&self, labour_update: &LabourUpdateReadModel) -> Result<()> {
        let row = LabourUpdateRow::from_read_model(labour_update)
            .context("Failed to convert labour_update to row")?;

        let bindings = vec![
            row.labour_update_id.into(),
            row.labour_id.into(),
            row.labour_update_type.into(),
            row.message.into(),
            row.edited.into(),
            row.application_generated.into(),
            row.created_at.into(),
            row.updated_at.into(),
        ];

        self.sql
            .exec(
                "INSERT OR REPLACE INTO labour_updates (
                    labour_update_id, labour_id, labour_update_type, message,
                    edited, application_generated, created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)",
                Some(bindings),
            )
            .context("Failed to overwrite labour_update")?;

        Ok(())
    }
}
