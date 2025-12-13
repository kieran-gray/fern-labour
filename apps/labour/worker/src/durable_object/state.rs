use anyhow::{Context, Result};

use worker::State;

use fern_labour_event_sourcing_rs::{
    AggregateRepository, AsyncProjector, CheckpointRepository, SyncProjector,
};

use crate::durable_object::{
    read_side::{
        QueryService,
        async_projection_processor::AsyncProjectionProcessor,
        checkpoint_repository::SqlCheckpointRepository,
        read_models::{
            contractions::{
                ContractionReadModelProjector, ContractionReadModelQuery, SqlContractionRepository,
            },
            labour::{LabourReadModelProjector, LabourReadModelQuery, SqlLabourRepository},
            labour_updates::{
                LabourUpdateReadModelProjector, LabourUpdateReadModelQuery,
                SqlLabourUpdateRepository,
            },
        },
        sync_projection_processor::SyncProjectionProcessor,
    },
    write_side::{
        application::{AdminCommandProcessor, command_processors::LabourCommandProcessor},
        domain::LabourEvent,
        infrastructure::SqlEventStore,
    },
};

pub struct WriteModel {
    pub labour_command_processor: LabourCommandProcessor,
    pub admin_command_processor: AdminCommandProcessor,
}

pub struct ReadModel {
    pub query_service: QueryService,
    pub labour_query: LabourReadModelQuery,
    pub contraction_query: ContractionReadModelQuery,
    pub labour_update_query: LabourUpdateReadModelQuery,
}

pub struct AsyncProcessors {
    pub async_projection_processor: AsyncProjectionProcessor,
    pub sync_projection_processor: SyncProjectionProcessor,
}

pub struct AggregateServices {
    write_model: WriteModel,
    read_model: ReadModel,
    async_processors: AsyncProcessors,
}

impl AggregateServices {
    fn build_write_model(state: &State) -> Result<WriteModel> {
        let sql = state.storage().sql();
        let event_store = SqlEventStore::create(sql.clone());
        event_store
            .init_schema()
            .context("Event store initialization failed")?;

        let repository = AggregateRepository::new(event_store.clone());
        let labour_command_processor = LabourCommandProcessor::new(repository);

        let checkpoint_repository = Box::new(SqlCheckpointRepository::create(sql.clone()));
        checkpoint_repository.init_schema()?;

        let admin_command_processor = AdminCommandProcessor::create(checkpoint_repository);

        Ok(WriteModel {
            labour_command_processor,
            admin_command_processor,
        })
    }

    fn build_read_model(state: &State) -> Result<ReadModel> {
        let sql = state.storage().sql();
        let query_service = QueryService::new(SqlEventStore::create(sql.clone()));

        let labour_repository = Box::new(SqlLabourRepository::create(sql.clone()));
        let labour_query = LabourReadModelQuery::create(labour_repository);

        let contraction_repository = Box::new(SqlContractionRepository::create(sql.clone()));
        let contraction_query = ContractionReadModelQuery::create(contraction_repository);

        let labour_update_repository = Box::new(SqlLabourUpdateRepository::create(sql.clone()));
        let labour_update_query = LabourUpdateReadModelQuery::create(labour_update_repository);

        Ok(ReadModel {
            query_service,
            labour_query,
            contraction_query,
            labour_update_query,
        })
    }

    fn build_sync_projection_processor(state: &State) -> Result<SyncProjectionProcessor> {
        let sql = state.storage().sql();
        let event_store = SqlEventStore::create(sql.clone());

        let checkpoint_repository = Box::new(SqlCheckpointRepository::create(sql.clone()));
        checkpoint_repository.init_schema()?;

        let labour_repository = Box::new(SqlLabourRepository::create(sql.clone()));
        labour_repository.init_schema()?;

        let labour_projector = Box::new(LabourReadModelProjector::create(labour_repository));

        let contraction_repository = Box::new(SqlContractionRepository::create(sql.clone()));
        contraction_repository.init_schema()?;

        let contraction_projector = Box::new(ContractionReadModelProjector::create(
            contraction_repository,
        ));

        let labour_update_repository = Box::new(SqlLabourUpdateRepository::create(sql.clone()));
        labour_update_repository.init_schema()?;

        let labour_update_projector = Box::new(LabourUpdateReadModelProjector::create(
            labour_update_repository,
        ));

        let projectors: Vec<Box<dyn SyncProjector<LabourEvent>>> = vec![
            labour_projector,
            contraction_projector,
            labour_update_projector,
        ];

        Ok(SyncProjectionProcessor::create(
            event_store,
            checkpoint_repository,
            projectors,
        ))
    }

    fn build_async_projection_processor(state: &State) -> Result<AsyncProjectionProcessor> {
        let sql = state.storage().sql();
        let event_store = SqlEventStore::create(sql.clone());

        let projectors: Vec<Box<dyn AsyncProjector<LabourEvent>>> = vec![];
        Ok(AsyncProjectionProcessor::create(event_store, projectors))
    }

    fn build_async_processors(state: &State) -> Result<AsyncProcessors> {
        let async_projection_processor = Self::build_async_projection_processor(state)?;
        let sync_projection_processor = Self::build_sync_projection_processor(state)?;
        Ok(AsyncProcessors {
            async_projection_processor,
            sync_projection_processor,
        })
    }

    pub fn from_worker_state(state: &State) -> Result<Self> {
        let write_model = Self::build_write_model(state)?;
        let read_model = Self::build_read_model(state)?;
        let async_processors = Self::build_async_processors(state)?;

        Ok(Self {
            write_model,
            read_model,
            async_processors,
        })
    }

    pub fn write_model(&self) -> &WriteModel {
        &self.write_model
    }

    pub fn read_model(&self) -> &ReadModel {
        &self.read_model
    }

    pub fn async_processors(&self) -> &AsyncProcessors {
        &self.async_processors
    }
}
