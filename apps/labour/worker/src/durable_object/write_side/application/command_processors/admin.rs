use anyhow::{Result, anyhow};
use fern_labour_event_sourcing_rs::{CheckpointRepository, CommandEnvelope};
use fern_labour_labour_shared::AdminCommand;
use tracing::info;

pub struct AdminCommandProcessor {
    checkpoint_repository: Box<dyn CheckpointRepository>,
}

impl AdminCommandProcessor {
    pub fn create(checkpoint_repository: Box<dyn CheckpointRepository>) -> Self {
        Self {
            checkpoint_repository,
        }
    }

    pub fn handle(&self, command_envelope: CommandEnvelope<AdminCommand>) -> Result<()> {
        info!(user_id = %command_envelope.metadata.user_id, "Processing admin command");

        match command_envelope.command {
            AdminCommand::RebuildReadModels { aggregate_id } => {
                info!(
                    aggregate_id = %aggregate_id,
                    "Rebuilding read models"
                );
                let result = self
                    .checkpoint_repository
                    .get_all_checkpoints()?
                    .iter()
                    .map(|c| {
                        self.checkpoint_repository
                            .reset_checkpoint(&c.projector_name)
                    })
                    .all(|r| r.is_ok());
                
                match result {
                    true => Ok(()),
                    false => Err(anyhow!("Failed to reset checkpoints")),
                }
            }
        }
    }
}
