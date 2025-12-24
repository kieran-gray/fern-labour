use anyhow::{Result, anyhow};
use fern_labour_event_sourcing_rs::{Aggregate, AggregateRepository};
use fern_labour_workers_shared::User;

use crate::durable_object::{
    authorization::{Action, Authorizer, resolve_principal},
    write_side::domain::{Labour, LabourCommand},
};

#[derive(Clone)]
pub struct LabourCommandProcessor {
    repository: AggregateRepository<Labour>,
    authorizer: Authorizer,
}

impl LabourCommandProcessor {
    pub fn new(repository: AggregateRepository<Labour>) -> Self {
        Self {
            repository,
            authorizer: Authorizer::new(),
        }
    }

    pub fn handle_command(&self, command: LabourCommand, user: User) -> Result<()> {
        let aggregate = self.repository.load()?;

        let principal = resolve_principal(&user, aggregate.as_ref());
        let action = Action::Command(command.clone());

        self.authorizer
            .authorize(&principal, &action, aggregate.as_ref())
            .map_err(|e| anyhow!("Authorization failed: {}", e))?;

        let events = Labour::handle_command(aggregate.as_ref(), command)
            .map_err(|e| anyhow!("Domain error: {}", e))?;

        if events.is_empty() {
            return Ok(());
        }

        self.repository.save(&events, user.user_id)?;

        Ok(())
    }
}
