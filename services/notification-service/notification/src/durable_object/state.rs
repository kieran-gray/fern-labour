use std::{cell::RefCell, rc::Rc};

use anyhow::{Context, Result};
use fern_labour_notifications_shared::{
    QueueMessage, QueueProducerTrait,
    service_clients::{DispatchClient, GenerationClient},
};
use fern_labour_workers_shared::{
    NotificationQueueProducer,
    clients::{FetcherDispatchClient, FetcherGenerationClient},
};
use worker::{Env, State};

use fern_labour_event_sourcing_rs::{AggregateRepository, CommandEnvelope, Projector};

use crate::{
    durable_object::{
        read_side::{
            QueryService,
            projection_processor::ProjectionProcessor,
            projectors::{
                notification_detail::NotificationDetailProjector,
                notification_status::NotificationStatusProjector,
            },
        },
        write_side::{
            application::{
                AdminCommandProcessor, PolicyEngine,
                command_processors::{NotificationCommandProcessor, ServiceCommandProcessor},
            },
            domain::NotificationEvent,
            infrastructure::{
                PolicyApplicationTracker, SqlEventStore,
                event_reaction_processor::EventReactionProcessor,
            },
        },
    },
    read_models::{
        notification_detail::D1NotificationDetailRepository,
        notification_status::D1NotificationStatusRepository,
    },
};

pub struct WriteModel {
    pub notification_command_processor: NotificationCommandProcessor,
    pub admin_command_processor: AdminCommandProcessor,
}

pub struct ReadModel {
    pub query_service: QueryService,
}

pub struct AsyncProcessors {
    pub event_processor: EventReactionProcessor,
    pub projection_processor: ProjectionProcessor,
}

pub struct AggregateServices {
    write_model: WriteModel,
    read_model: ReadModel,
    async_processors: RefCell<Option<Rc<AsyncProcessors>>>,
}

impl AggregateServices {
    fn create_command_bus(
        env: &Env,
    ) -> Result<Box<dyn QueueProducerTrait<Envelope = CommandEnvelope<QueueMessage>>>> {
        let queue = env
            .queue("NOTIFICATION_COMMAND_BUS")
            .context("Failed to load command bus")?;
        Ok(NotificationQueueProducer::create(queue))
    }

    fn create_notification_status_projector(env: &Env) -> Result<Box<NotificationStatusProjector>> {
        let binding = "NOTIFICATION_STATUS_DB";
        let db = env
            .d1(binding)
            .context(format!("Failed to load {}", binding))?;
        let repository = Box::new(D1NotificationStatusRepository::create(db));
        Ok(Box::new(NotificationStatusProjector::create(repository)))
    }

    fn create_notification_detail_projector(env: &Env) -> Result<Box<NotificationDetailProjector>> {
        let binding = "NOTIFICATION_DETAIL_DB";
        let db = env
            .d1(binding)
            .context(format!("Failed to load {}", binding))?;
        let repository = Box::new(D1NotificationDetailRepository::create(db));
        Ok(Box::new(NotificationDetailProjector::create(repository)))
    }

    fn create_dispatch_client(env: &Env) -> Result<Box<dyn DispatchClient>> {
        let dispatch_fetcher = env
            .service("DISPATCH_SERVICE_API")
            .context("Missing binding DISPATCH_SERVICE_API")?;

        Ok(Box::new(FetcherDispatchClient::create(dispatch_fetcher)))
    }

    fn create_generation_client(env: &Env) -> Result<Box<dyn GenerationClient>> {
        let generation_fetcher = env
            .service("GENERATION_SERVICE_API")
            .context("Missing binding GENERATION_SERVICE_API")?;

        Ok(Box::new(FetcherGenerationClient::create(
            generation_fetcher,
        )))
    }

    fn build_write_model(state: &State) -> Result<WriteModel> {
        let sql = state.storage().sql();
        let event_store = SqlEventStore::create(sql.clone());
        event_store
            .init_schema()
            .context("Event store initialization failed")?;

        let repository = AggregateRepository::new(event_store.clone());
        let notification_command_processor = NotificationCommandProcessor::new(repository);

        let admin_command_processor = AdminCommandProcessor::create();

        Ok(WriteModel {
            notification_command_processor,
            admin_command_processor,
        })
    }

    fn build_read_model(state: &State) -> Result<ReadModel> {
        let query_service = QueryService::new(SqlEventStore::create(state.storage().sql()));

        Ok(ReadModel { query_service })
    }

    fn build_async_processors(state: &State, env: &Env) -> Result<AsyncProcessors> {
        let sql = state.storage().sql();
        let event_store = SqlEventStore::create(sql.clone());

        let command_bus = Self::create_command_bus(env)?;

        let notification_status_projector = Self::create_notification_status_projector(env)?;
        let notification_detail_projector = Self::create_notification_detail_projector(env)?;
        let projectors: Vec<Box<dyn Projector<NotificationEvent>>> =
            vec![notification_detail_projector, notification_status_projector];
        let projection_processor = ProjectionProcessor::create(event_store.clone(), projectors);

        let policy_application_tracker = PolicyApplicationTracker::create(sql.clone());
        policy_application_tracker
            .init_schema()
            .context("Event processing tracker initialization failed")?;

        let policy_engine = PolicyEngine::new();

        let generation_client = Self::create_generation_client(env)?;
        let dispatch_client = Self::create_dispatch_client(env)?;
        let service_command_processor =
            ServiceCommandProcessor::create(command_bus, generation_client, dispatch_client);

        let repository = AggregateRepository::new(event_store.clone());
        let notification_command_processor = NotificationCommandProcessor::new(repository);

        let event_processor = EventReactionProcessor::create(
            event_store,
            policy_application_tracker,
            policy_engine,
            notification_command_processor,
            service_command_processor,
        );

        Ok(AsyncProcessors {
            event_processor,
            projection_processor,
        })
    }

    pub fn from_worker_state(state: &State) -> Result<Self> {
        let write_model = Self::build_write_model(state)?;
        let read_model = Self::build_read_model(state)?;

        Ok(Self {
            write_model,
            read_model,
            async_processors: RefCell::new(None),
        })
    }

    pub fn write_model(&self) -> &WriteModel {
        &self.write_model
    }

    pub fn read_model(&self) -> &ReadModel {
        &self.read_model
    }

    pub fn async_processors(&self, state: &State, env: &Env) -> Result<()> {
        if self.async_processors.borrow().is_none() {
            let services = Self::build_async_processors(state, env)?;
            *self.async_processors.borrow_mut() = Some(Rc::new(services));
        }
        Ok(())
    }

    pub fn get_async_processors(&self) -> Rc<AsyncProcessors> {
        self.async_processors
            .borrow()
            .as_ref()
            .expect("alarm_services not initialized")
            .clone()
    }
}
