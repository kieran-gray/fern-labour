use anyhow::{Context, Result, anyhow};

use worker::{Env, State};

use fern_labour_event_sourcing_rs::{
    AggregateRepository, AsyncProjector, CheckpointRepository, SyncProjector,
};

use crate::durable_object::{
    read_side::{
        checkpoint_repository::SqlCheckpointRepository,
        projection_processors::{
            async_processor::AsyncProjectionProcessor, sync_processor::SyncProjectionProcessor,
        },
        read_models::{
            contractions::{
                ContractionReadModelProjector, ContractionReadModelQuery, SqlContractionRepository,
            },
            events::query::EventQuery,
            labour::{LabourReadModelProjector, LabourReadModelQuery, SqlLabourRepository},
            labour_status::{D1LabourStatusRepository, LabourStatusReadModelProjector},
            labour_updates::{
                LabourUpdateReadModelProjector, LabourUpdateReadModelQuery,
                SqlLabourUpdateRepository,
            },
            subscriptions::{
                SqlSubscriptionRepository, SubscriptionReadModelProjector,
                SubscriptionReadModelQuery,
            },
        },
    },
    security::token_generator::{SplitMix64TokenGenerator, SubscriptionTokenGenerator},
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
    pub event_query: EventQuery,
    pub labour_query: LabourReadModelQuery,
    pub contraction_query: ContractionReadModelQuery,
    pub labour_update_query: LabourUpdateReadModelQuery,
    pub subscription_query: SubscriptionReadModelQuery,
    pub subscription_token_generator: Box<dyn SubscriptionTokenGenerator>,
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

    fn build_read_model(state: &State, env: &Env) -> Result<ReadModel> {
        let sql = state.storage().sql();
        let event_query = EventQuery::new(SqlEventStore::create(sql.clone()));

        let labour_repository = Box::new(SqlLabourRepository::create(sql.clone()));
        let labour_query = LabourReadModelQuery::create(labour_repository);

        let contraction_repository = Box::new(SqlContractionRepository::create(sql.clone()));
        let contraction_query = ContractionReadModelQuery::create(contraction_repository);

        let labour_update_repository = Box::new(SqlLabourUpdateRepository::create(sql.clone()));
        let labour_update_query = LabourUpdateReadModelQuery::create(labour_update_repository);

        let subscription_repository = Box::new(SqlSubscriptionRepository::create(sql.clone()));
        let subscription_query = SubscriptionReadModelQuery::create(subscription_repository);

        let subscription_token_salt: String = env
            .var("SUBSCRIPTION_TOKEN_SALT")
            .map_err(|e| anyhow!("Missing env binding: {e}"))?
            .to_string();

        let subscription_token_generator =
            Box::new(SplitMix64TokenGenerator::create(subscription_token_salt));

        Ok(ReadModel {
            event_query,
            labour_query,
            contraction_query,
            labour_update_query,
            subscription_query,
            subscription_token_generator,
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

        let subscription_repository = Box::new(SqlSubscriptionRepository::create(sql.clone()));
        subscription_repository.init_schema()?;

        let subscription_projector = Box::new(SubscriptionReadModelProjector::create(
            subscription_repository,
        ));

        let projectors: Vec<Box<dyn SyncProjector<LabourEvent>>> = vec![
            labour_projector,
            contraction_projector,
            labour_update_projector,
            subscription_projector,
        ];

        Ok(SyncProjectionProcessor::create(
            event_store,
            checkpoint_repository,
            projectors,
        ))
    }

    fn build_async_projection_processor(
        state: &State,
        env: &Env,
    ) -> Result<AsyncProjectionProcessor> {
        let sql = state.storage().sql();
        let event_store = SqlEventStore::create(sql.clone());

        let binding = "READ_MODEL_DB";
        let db = env
            .d1(binding)
            .context(format!("Failed to load {}", binding))?;
        let repository = Box::new(D1LabourStatusRepository::create(db));
        let labour_status_projector = Box::new(LabourStatusReadModelProjector::create(repository));

        let projectors: Vec<Box<dyn AsyncProjector<LabourEvent>>> = vec![labour_status_projector];
        Ok(AsyncProjectionProcessor::create(event_store, projectors))
    }

    fn build_async_processors(state: &State, env: &Env) -> Result<AsyncProcessors> {
        let async_projection_processor = Self::build_async_projection_processor(state, env)?;
        let sync_projection_processor = Self::build_sync_projection_processor(state)?;
        Ok(AsyncProcessors {
            async_projection_processor,
            sync_projection_processor,
        })
    }

    pub fn from_worker_state(state: &State, env: &Env) -> Result<Self> {
        let write_model = Self::build_write_model(state)?;
        let read_model = Self::build_read_model(state, env)?;
        let async_processors = Self::build_async_processors(state, env)?;

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
