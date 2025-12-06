use std::rc::Rc;

use anyhow::{Context, Result};
use fern_labour_event_sourcing_rs::{AggregateRepository, EventStoreTrait, StoredEventRow};
use fern_labour_notifications_shared::ServiceCommand;
use tracing::{debug, error, info};

use crate::durable_object::write_side::{
    application::{
        PolicyEngine,
        command_processors::{NotificationCommandProcessor, ServiceCommandProcessor},
    },
    domain::{Labour, NotificationEvent},
    infrastructure::{
        PolicyApplicationTracker, persistence::policy_application_tracker::ProcessingStatus,
    },
};

const MAX_RETRIES: i64 = 3;

pub struct EventReactionProcessor {
    event_store: Rc<dyn EventStoreTrait>,
    repository: AggregateRepository<Labour>,
    policy_application_tracker: PolicyApplicationTracker,
    policy_engine: PolicyEngine,
    notification_command_processor: NotificationCommandProcessor,
    service_command_processor: ServiceCommandProcessor,
}

/*
Some thoughts.

Previously, we had a command inbox that was processed in the fetch handler.
At the end of processing a successful fetch request we would have an event stored
in the event store, the fetch handler then also ran the event through the policy engine
to generate service commands that were added to the outbox for later processing.

The alarm would then run immediately after the fetch returned to process the outbox commands.

This had two benefits:
1. The fetch handler avoided async calls, which can introduce race conditions and remove
   some of the cool Durable Object protections (input/output gates).
2. The fetch handler and alarm processing were basically completely separate. Fetch added
   to the outbox, alarm read from it. There was no place for any conflicts to possibly take place.

But it did have an issue, which is that it was potentially possible to save the event in the event
store but not save the resulting command in the outbox (dual write problem). The DO output gates
are supposed to protect against this kind of error, but I have tested this and I think that they
just protect against Cloudflare storage issues, not your code panicking/erroring.

Now I have refactored the system to treat the event store as the source-of-truth. We read from the
event store and if we have not yet processed the event, then we process it. This is simpler and,
in my opinion, easier to understand.

I also added the ability to have high priority notification that skip the queue and are processed
in real time in the alarm. We take events from the event store, run them through the policy engine,
execute these commands immediately, and feed the events back into the system again.

This means we can go in the following loop:

Fetch Handler:
RequestNotification (command) -> Command Handler -> NotificationRequested (event)

Alarm:
Loop 1:
NotificationRequested (event) -> Policy Engine ->
RenderNotification (command) -> Direct Service Call ->
StoreRenderedContent (command) -> Command Handler -> RenderedContentStored (event)

Loop 2:
RenderedContentStored (event) -> Policy Engine ->
DispatchNotification (command) -> Direct Service Call ->
MarkAsDispatched (command) -> Command Handler -> NotificationDispatched (event)

Loop 3:
NotificationDispatched (event) -> Policy Engine -> No commands -> Done.

This service is already way overkill for sending an email, I'm not dealing with the race conditions
here. I don't think they will ever happen realistically.
*/
impl EventReactionProcessor {
    pub fn create(
        event_store: Rc<dyn EventStoreTrait>,
        policy_application_tracker: PolicyApplicationTracker,
        policy_engine: PolicyEngine,
        notification_command_processor: NotificationCommandProcessor,
        service_command_processor: ServiceCommandProcessor,
    ) -> Self {
        let repository = AggregateRepository::new(event_store.clone());

        Self {
            event_store,
            repository,
            policy_application_tracker,
            policy_engine,
            notification_command_processor,
            service_command_processor,
        }
    }

    pub async fn process_events(&self) -> Result<()> {
        info!("Starting event processing loop");

        loop {
            let last_processed = self
                .policy_application_tracker
                .get_last_processed_sequence()
                .context("Failed to get last processed sequence")?
                .unwrap_or(0);

            let next_event_result = self.event_store.events_since(last_processed, 1)?;
            let next_event = match next_event_result.first() {
                Some(event) => event,
                None => {
                    debug!("Outbox empty, processing complete");
                    break;
                }
            };

            let entry = self
                .policy_application_tracker
                .get_or_create_entry(next_event.sequence)
                .context("Failed to get or create processing entry")?;

            if entry.retry_count >= MAX_RETRIES {
                error!(
                    sequence = next_event.sequence,
                    retries = entry.retry_count,
                    last_error = ?entry.last_error,
                    "Event exceeded max retries - skipping"
                );
                continue;
            }
            if entry.status == ProcessingStatus::PROCESSED {
                debug!(
                    sequence = next_event.sequence,
                    "Event already processed, skipping"
                );
                continue;
            }

            match self.process_event(next_event).await {
                Ok(()) => {
                    self.policy_application_tracker
                        .mark_completed(next_event.sequence)
                        .context("Failed to mark event as completed")?;
                    info!(
                        sequence = next_event.sequence,
                        "Event processed successfully"
                    );
                }
                Err(err) => {
                    error!(
                        sequence = next_event.sequence,
                        error = %err,
                        "Failed to process event"
                    );
                    self.policy_application_tracker
                        .increment_retry(next_event.sequence, &err.to_string())
                        .context("Failed to increment retry count")?;
                }
            }
        }
        Ok(())
    }

    async fn process_event(&self, next_event: &StoredEventRow) -> Result<()> {
        let aggregate = self.repository.load()?;
        let priority = aggregate.as_ref().map(|a| a.is_priority()).unwrap_or(false);

        let event: NotificationEvent =
            serde_json::from_str(&next_event.event_data).context("Failed to deserialize event")?;

        let service_commands = self
            .policy_engine
            .apply_policies(&event, aggregate.as_ref());

        self.handle_service_commands(service_commands, priority)
            .await
    }

    async fn handle_service_commands(
        &self,
        commands: Vec<ServiceCommand>,
        priority: bool,
    ) -> Result<()> {
        for command in commands {
            if priority {
                let notification_command = self
                    .service_command_processor
                    .handle_priority(command)
                    .await?;
                self.notification_command_processor
                    .handle_command(notification_command, "notification".to_string())?;
            } else {
                self.service_command_processor.handle(command).await?;
            }
        }
        Ok(())
    }
}
