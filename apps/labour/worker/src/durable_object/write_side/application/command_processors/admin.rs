use anyhow::Result;
use fern_labour_event_sourcing_rs::CommandEnvelope;
use fern_labour_notifications_shared::AdminCommand;
use tracing::info;

pub struct AdminCommandProcessor;

impl AdminCommandProcessor {
    pub fn create() -> Self {
        Self
    }

    pub fn handle(&self, command_envelope: CommandEnvelope<AdminCommand>) -> Result<()> {
        info!(user_id = %command_envelope.metadata.user_id, "Processing admin command");

        match command_envelope.command {
            AdminCommand::RebuildReadModels { aggregate_id } => {
                info!(
                    aggregate_id = %aggregate_id,
                    "Rebuilding read models"
                );
                Ok(())
            }
        }
    }
}
