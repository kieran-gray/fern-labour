use anyhow::{Result, anyhow};
use fern_labour_event_sourcing_rs::{Aggregate, AggregateRepository};
use fern_labour_workers_shared::User;

use crate::durable_object::write_side::domain::{Labour, LabourCommand};

#[derive(Clone)]
pub struct LabourCommandProcessor {
    repository: AggregateRepository<Labour>,
}

impl LabourCommandProcessor {
    pub fn new(repository: AggregateRepository<Labour>) -> Self {
        Self { repository }
    }

    pub fn handle_command(&self, command: LabourCommand, user: User) -> Result<()> {
        let aggregate = self.repository.load()?;

        let events = Labour::handle_command(aggregate.as_ref(), command)
            .map_err(|e| anyhow!("Domain error: {}", e))?;

        if events.is_empty() {
            return Ok(());
        }

        self.repository.save(&events, user.user_id)?;

        Ok(())
    }
}
