use anyhow::{Context, Result, anyhow};
use fern_labour_event_sourcing_rs::{DecodedCursor, SyncRepositoryTrait};
use uuid::Uuid;
use worker::SqlStorage;

use super::read_model::{ContractionReadModel, ContractionRow};

pub struct SqlContractionRepository {
    sql: SqlStorage,
}

impl SqlContractionRepository {
    pub fn create(sql: SqlStorage) -> Self {
        Self { sql }
    }

    pub fn init_schema(&self) -> Result<()> {
        self.sql
            .exec(
                "CREATE TABLE IF NOT EXISTS contractions (
                    contraction_id TEXT PRIMARY KEY,
                    labour_id TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    intensity TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )",
                None,
            )
            .map_err(|err| anyhow!("Failed to create contractions table: {err}"))?;

        self.sql
            .exec(
                "CREATE INDEX IF NOT EXISTS idx_contractions_updated_at
                 ON contractions(updated_at DESC)",
                None,
            )
            .context("Failed to create updated_at index")?;

        Ok(())
    }

    pub fn get_all(&self) -> Result<Vec<ContractionReadModel>> {
        let rows: Vec<ContractionRow> = self
            .sql
            .exec("SELECT * FROM contractions ORDER BY created_at ASC", None)
            .context("Failed to execute contractions query")?
            .to_array()
            .context("Failed to fetch contractions")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }

    pub fn get_by_labour_id(&self, labour_id: Uuid) -> Result<Vec<ContractionReadModel>> {
        let rows: Vec<ContractionRow> = self
            .sql
            .exec(
                "SELECT * FROM contractions WHERE labour_id = ?1 ORDER BY created_at ASC",
                Some(vec![labour_id.to_string().into()]),
            )
            .context("Failed to execute contractions query")?
            .to_array()
            .context("Failed to fetch contractions")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }
}

impl SyncRepositoryTrait<ContractionReadModel> for SqlContractionRepository {
    fn get_by_id(&self, contraction_id: Uuid) -> Result<ContractionReadModel> {
        let rows: Vec<ContractionRow> = self
            .sql
            .exec(
                "SELECT * FROM contractions WHERE contraction_id = ?1",
                Some(vec![contraction_id.to_string().into()]),
            )
            .context("Failed to execute contraction query")?
            .to_array()
            .context("Failed to fetch contraction")?;

        match rows.into_iter().next() {
            Some(row) => row.into_read_model(),
            None => Err(anyhow::anyhow!("Contraction not found")),
        }
    }

    fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<ContractionReadModel>> {
        let mut query = "SELECT * FROM contractions".to_string();
        let mut bindings = vec![];

        if let Some(cur) = cursor {
            query.push_str(" WHERE updated_at < ?1 OR (updated_at = ?1 AND contraction_id < ?2)");
            bindings.push(cur.last_updated_at.to_rfc3339().into());
            bindings.push(cur.last_id.to_string().into());
        }

        let limit_param_index = bindings.len() + 1;
        query.push_str(&format!(
            " ORDER BY updated_at DESC, contraction_id DESC LIMIT ?{}",
            limit_param_index
        ));

        let plus_one_limit = limit + 1;
        bindings.push((plus_one_limit as f64).into());

        let rows: Vec<ContractionRow> = self
            .sql
            .exec(&query, Some(bindings))
            .context("Failed to execute contractions query")?
            .to_array()
            .context("Failed to fetch contractions")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }

    fn upsert(&self, contraction: &ContractionReadModel) -> Result<()> {
        let row = ContractionRow::from_read_model(contraction)
            .context("Failed to convert contraction to row")?;

        let mut bindings = vec![
            row.contraction_id.into(),
            row.labour_id.into(),
            row.duration.into(),
        ];

        bindings.push(match row.intensity {
            Some(intensity) => intensity.into(),
            None => worker::SqlStorageValue::Null,
        });

        bindings.push(row.created_at.into());
        bindings.push(row.updated_at.into());

        self.sql
            .exec(
                "INSERT INTO contractions (
                    contraction_id, labour_id, duration, intensity,
                    created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6)
                 ON CONFLICT(contraction_id)
                 DO UPDATE SET
                    duration = ?3,
                    intensity = ?4,
                    updated_at = ?6",
                Some(bindings),
            )
            .context("Failed to upsert contraction")?;

        Ok(())
    }

    fn delete(&self, contraction_id: Uuid) -> Result<()> {
        self.sql
            .exec(
                "DELETE FROM contractions WHERE contraction_id = ?1",
                Some(vec![contraction_id.to_string().into()]),
            )
            .context("Failed to delete contraction")?;

        Ok(())
    }

    fn overwrite(&self, contraction: &ContractionReadModel) -> Result<()> {
        let row = ContractionRow::from_read_model(contraction)
            .context("Failed to convert contraction to row")?;

        let mut bindings = vec![
            row.contraction_id.into(),
            row.labour_id.into(),
            row.duration.into(),
        ];

        bindings.push(match row.intensity {
            Some(intensity) => intensity.into(),
            None => worker::SqlStorageValue::Null,
        });

        bindings.push(row.created_at.into());
        bindings.push(row.updated_at.into());

        self.sql
            .exec(
                "INSERT OR REPLACE INTO contractions (
                    contraction_id, labour_id, duration, intensity,
                    created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
                Some(bindings),
            )
            .context("Failed to overwrite contraction")?;

        Ok(())
    }
}
