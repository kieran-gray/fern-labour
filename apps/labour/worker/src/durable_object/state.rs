use anyhow::{Context, Result};

use worker::State;

use fern_labour_event_sourcing_rs::{AggregateRepository, Projector};

use crate::durable_object::{
    read_side::{
        QueryService,
        projection_processor::ProjectionProcessor,
        read_models::labour::{LabourReadModelProjector, SqlLabourRepository},
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
}

pub struct AsyncProcessors {
    pub projection_processor: ProjectionProcessor,
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

        let admin_command_processor = AdminCommandProcessor::create();

        Ok(WriteModel {
            labour_command_processor,
            admin_command_processor,
        })
    }

    fn build_read_model(state: &State) -> Result<ReadModel> {
        let query_service = QueryService::new(SqlEventStore::create(state.storage().sql()));

        Ok(ReadModel { query_service })
    }

    fn build_async_processors(state: &State) -> Result<AsyncProcessors> {
        let sql = state.storage().sql();
        let event_store = SqlEventStore::create(sql.clone());
        let labour_repository = Box::new(SqlLabourRepository::create(sql));
        labour_repository
            .init_schema()
            .context("Labour repository initialization failed")?;

        let labour_projector = Box::new(LabourReadModelProjector::create(labour_repository));
        let projectors: Vec<Box<dyn Projector<LabourEvent>>> = vec![labour_projector];
        let projection_processor = ProjectionProcessor::create(event_store, projectors);
        Ok(AsyncProcessors {
            projection_processor,
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
