use anyhow::{Result, anyhow};
use fern_labour_event_sourcing_rs::{Aggregate, AggregateRepository};

use crate::durable_object::write_side::domain::{Notification, NotificationCommand};

pub struct NotificationCommandProcessor {
    repository: AggregateRepository<Notification>,
}

impl NotificationCommandProcessor {
    pub fn new(repository: AggregateRepository<Notification>) -> Self {
        Self { repository }
    }

    pub fn handle_command(&self, command: NotificationCommand, user_id: String) -> Result<()> {
        let aggregate = self.repository.load()?;

        let events = Notification::handle_command(aggregate.as_ref(), command)
            .map_err(|e| anyhow!("Domain error: {}", e))?;

        if events.is_empty() {
            return Ok(());
        }

        self.repository.save(&events, user_id)?;
        Ok(())
    }
}
