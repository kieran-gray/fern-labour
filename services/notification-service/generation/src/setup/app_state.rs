use anyhow::{Context, Result};
use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::{QueueMessage, QueueProducerTrait};
use fern_labour_workers_shared::NotificationQueueProducer;
use worker::Env;

use crate::{
    application::template_engine::TemplateEngineTrait,
    infrastructure::template_engine::TinyTemplateEngine,
};

pub struct AppState {
    pub template_engine: Box<dyn TemplateEngineTrait>,
    pub command_producer: Box<dyn QueueProducerTrait<Envelope = CommandEnvelope<QueueMessage>>>,
}

impl AppState {
    fn create_command_producer(
        env: &Env,
    ) -> Result<Box<dyn QueueProducerTrait<Envelope = CommandEnvelope<QueueMessage>>>> {
        let queue = env
            .queue("NOTIFICATION_COMMAND_BUS")
            .context("Failed to load command bus")?;
        Ok(NotificationQueueProducer::create(queue))
    }

    pub fn from_env(env: &Env) -> Result<Self> {
        let template_engine = Box::new(TinyTemplateEngine::new());

        let command_producer = Self::create_command_producer(env)?;

        Ok(Self {
            template_engine,
            command_producer,
        })
    }
}
