use anyhow::{Result, anyhow};
use fern_labour_event_sourcing_rs::{Aggregate, AggregateRepository};

use crate::durable_object::write_side::domain::{Labour, NotificationCommand};

pub struct NotificationCommandProcessor {
    repository: AggregateRepository<Labour>,
}

impl NotificationCommandProcessor {
    pub fn new(repository: AggregateRepository<Labour>) -> Self {
        Self { repository }
    }

    pub fn handle_command(&self, command: NotificationCommand, user_id: String) -> Result<()> {
        let aggregate = self.repository.load()?;

        let events = Labour::handle_command(aggregate.as_ref(), command)
            .map_err(|e| anyhow!("Domain error: {}", e))?;

        if events.is_empty() {
            return Ok(());
        }

        self.repository.save(&events, user_id)?;
        Ok(())
    }
}
