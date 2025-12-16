use anyhow::{Context, Result, anyhow};
use async_trait::async_trait;
use fern_labour_event_sourcing_rs::{
    AsyncRepositoryTrait, AsyncRepositoryUserTrait, DecodedCursor,
};
use uuid::Uuid;
use worker::D1Database;

use super::read_model::{LabourStatusReadModel, LabourStatusRow};

#[async_trait(?Send)]
pub trait LabourStatusRepositoryTrait:
    AsyncRepositoryTrait<LabourStatusReadModel> + AsyncRepositoryUserTrait<LabourStatusReadModel>
{
    async fn get_active_labour(&self, user_id: String) -> Result<Option<LabourStatusReadModel>>;
    async fn get_by_ids(&self, labour_ids: Vec<Uuid>) -> Result<Vec<LabourStatusReadModel>>;
}

pub struct D1LabourStatusRepository {
    db: D1Database,
}

impl D1LabourStatusRepository {
    pub fn create(db: D1Database) -> Self {
        Self { db }
    }
}

#[async_trait(?Send)]
impl AsyncRepositoryTrait<LabourStatusReadModel> for D1LabourStatusRepository {
    async fn get_by_id(&self, labour_id: Uuid) -> Result<LabourStatusReadModel> {
        let result: Option<LabourStatusRow> = self
            .db
            .prepare("SELECT * FROM labour_status WHERE labour_id = ?1")
            .bind(&[labour_id.to_string().into()])
            .context("Failed to prepare labour status query")?
            .first(None)
            .await
            .context("Failed to fetch labour status")?;

        match result {
            Some(row) => row.into_read_model(),
            None => Err(anyhow!("Labour status not found")),
        }
    }

    async fn get(
        &self,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<LabourStatusReadModel>> {
        let mut query = "SELECT * FROM labour_status".to_string();
        let mut bindings = vec![];

        if let Some(cur) = cursor {
            query.push_str(" WHERE updated_at < ?1 OR (updated_at = ?1 AND labour_id < ?2)");
            bindings.push(cur.last_updated_at.to_rfc3339().into());
            bindings.push(cur.last_id.to_string().into());
        }

        let limit_param_index = bindings.len() + 1;
        query.push_str(&format!(
            " ORDER BY updated_at DESC, labour_id DESC LIMIT ?{}",
            limit_param_index
        ));

        let plus_one_limit = limit + 1;
        bindings.push((plus_one_limit as f64).into());

        let statement = self
            .db
            .prepare(query)
            .bind(&bindings)
            .context("Failed to bind parameters")?;

        let rows: Vec<LabourStatusRow> = statement
            .all()
            .await
            .context("Failed to fetch labour status")?
            .results()
            .context("Failed to parse labour status results")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }

    async fn upsert(&self, labour: &LabourStatusReadModel) -> Result<()> {
        let labour_name_value = match &labour.labour_name {
            Some(name) => name.clone().into(),
            None => worker::wasm_bindgen::JsValue::NULL,
        };

        self.db
            .prepare(
                "INSERT INTO labour_status (
                    labour_id, mother_id, mother_name, current_phase, labour_name, created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)
                 ON CONFLICT(labour_id)
                 DO UPDATE SET
                    current_phase = ?4,
                    labour_name = ?5,
                    updated_at = ?7",
            )
            .bind(&[
                labour.labour_id.to_string().into(),
                labour.mother_id.clone().into(),
                labour.mother_name.clone().into(),
                labour.current_phase.to_string().into(),
                labour_name_value,
                labour.created_at.to_rfc3339().into(),
                labour.updated_at.to_rfc3339().into(),
            ])
            .context("Failed to prepare labour status upsert")?
            .run()
            .await
            .context("Failed to upsert labour status")?;

        Ok(())
    }

    async fn delete(&self, id: Uuid) -> Result<()> {
        match self
            .db
            .prepare(
                "DELETE FROM labour_status
                 WHERE labour_id = ?1;",
            )
            .bind(&[id.to_string().into()])
            .context("Failed to prepare labour status query")?
            .run()
            .await
            .context("Failed to delete labour status")
        {
            Ok(_) => Ok(()),
            Err(err) => Err(anyhow!(err.to_string())),
        }
    }

    async fn overwrite(&self, labour: &LabourStatusReadModel) -> Result<()> {
        let labour_name_value = match &labour.labour_name {
            Some(name) => name.clone().into(),
            None => worker::wasm_bindgen::JsValue::NULL,
        };

        self.db
            .prepare(
                "INSERT OR REPLACE INTO labour_status (
                    labour_id, mother_id, mother_name, current_phase, labour_name, created_at, updated_at
                 )
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            )
            .bind(&[
                labour.labour_id.to_string().into(),
                labour.mother_id.clone().into(),
                labour.mother_name.clone().into(),
                labour.current_phase.to_string().into(),
                labour_name_value,
                labour.created_at.to_rfc3339().into(),
                labour.updated_at.to_rfc3339().into(),
            ])
            .context("Failed to prepare labour status overwrite")?
            .run()
            .await
            .context("Failed to overwrite labour status")?;

        Ok(())
    }
}

#[async_trait(?Send)]
impl AsyncRepositoryUserTrait<LabourStatusReadModel> for D1LabourStatusRepository {
    async fn get_by_user_id(
        &self,
        user_id: String,
        limit: usize,
        cursor: Option<DecodedCursor>,
    ) -> Result<Vec<LabourStatusReadModel>> {
        let mut query = "SELECT * FROM labour_status WHERE mother_id = ?1".to_string();
        let mut bindings = vec![user_id.into()];

        if let Some(cur) = cursor {
            query.push_str(" WHERE updated_at < ?2 OR (updated_at = ?2 AND labour_id < ?3)");
            bindings.push(cur.last_updated_at.to_rfc3339().into());
            bindings.push(cur.last_id.to_string().into());
        }

        let limit_param_index = bindings.len() + 1;
        query.push_str(&format!(
            " ORDER BY updated_at DESC, labour_id DESC LIMIT ?{}",
            limit_param_index
        ));

        let plus_one_limit = limit + 1;
        bindings.push((plus_one_limit as f64).into());

        let statement = self
            .db
            .prepare(query)
            .bind(&bindings)
            .context("Failed to bind parameters")?;

        let rows: Vec<LabourStatusRow> = statement
            .all()
            .await
            .context("Failed to fetch labour status")?
            .results()
            .context("Failed to parse labour status results")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }
}

#[async_trait(?Send)]
impl LabourStatusRepositoryTrait for D1LabourStatusRepository {
    async fn get_active_labour(&self, user_id: String) -> Result<Option<LabourStatusReadModel>> {
        let result: Option<LabourStatusRow> = self
            .db
            .prepare(
                "SELECT * FROM labour_status WHERE mother_id = ?1 AND current_phase != 'COMPLETED'",
            )
            .bind(&[user_id.to_string().into()])
            .context("Failed to prepare active labour query")?
            .first(None)
            .await
            .context("Failed to fetch active labour")?;

        match result {
            Some(row) => Ok(Some(row.into_read_model()?)),
            None => Ok(None),
        }
    }

    async fn get_by_ids(&self, labour_ids: Vec<Uuid>) -> Result<Vec<LabourStatusReadModel>> {
        if labour_ids.is_empty() {
            return Ok(vec![]);
        }

        let placeholders: Vec<String> = (1..=labour_ids.len()).map(|i| format!("?{}", i)).collect();
        let query = format!(
            "SELECT * FROM labour_status WHERE labour_id IN ({})",
            placeholders.join(", ")
        );

        let bindings: Vec<worker::wasm_bindgen::JsValue> =
            labour_ids.iter().map(|id| id.to_string().into()).collect();

        let statement = self
            .db
            .prepare(query)
            .bind(&bindings)
            .context("Failed to bind parameters")?;

        let rows: Vec<LabourStatusRow> = statement
            .all()
            .await
            .context("Failed to fetch labour status")?
            .results()
            .context("Failed to parse labour status results")?;

        rows.into_iter().map(|row| row.into_read_model()).collect()
    }
}
