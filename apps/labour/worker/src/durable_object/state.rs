use anyhow::{Context, Result};

use worker::State;

use fern_labour_event_sourcing_rs::AggregateRepository;

use crate::durable_object::{
    read_side::QueryService,
    write_side::{
        application::{AdminCommandProcessor, command_processors::LabourCommandProcessor},
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

pub struct AggregateServices {
    write_model: WriteModel,
    read_model: ReadModel,
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

    pub fn from_worker_state(state: &State) -> Result<Self> {
        let write_model = Self::build_write_model(state)?;
        let read_model = Self::build_read_model(state)?;

        Ok(Self {
            write_model,
            read_model,
        })
    }

    pub fn write_model(&self) -> &WriteModel {
        &self.write_model
    }

    pub fn read_model(&self) -> &ReadModel {
        &self.read_model
    }
}
