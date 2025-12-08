use fern_labour_notifications_shared::ServiceCommand;
use tracing::debug;

use crate::durable_object::write_side::domain::{
    Notification, NotificationEvent,
    policies::{
        EventPolicy, notification_dispatch_policy::NotificationDispatchPolicy,
        notification_rendering_policy::NotificationRenderingPolicy,
    },
};

pub struct PolicyEngine {
    policies: Vec<Box<dyn EventPolicy>>,
}

impl Default for PolicyEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl PolicyEngine {
    pub fn new() -> Self {
        Self {
            policies: vec![
                Box::new(NotificationRenderingPolicy),
                Box::new(NotificationDispatchPolicy),
            ],
        }
    }

    pub fn apply(
        &self,
        events: &[NotificationEvent],
        aggregate_state: Option<&Notification>,
    ) -> Vec<ServiceCommand> {
        events
            .iter()
            .flat_map(|event| self.apply_policies(event, aggregate_state))
            .collect()
    }

    pub fn apply_policies(
        &self,
        event: &NotificationEvent,
        aggregate: Option<&Notification>,
    ) -> Vec<ServiceCommand> {
        debug!(
            event_type = ?event,
            policy_count = self.policies.len(),
            has_aggregate = aggregate.is_some(),
            "Evaluating policies for event"
        );

        let commands: Vec<ServiceCommand> = self
            .policies
            .iter()
            .flat_map(|policy| policy.handle(event, aggregate))
            .collect();

        debug!(
            event_type = ?event,
            commands_generated = commands.len(),
            command_types = ?commands.iter().map(std::mem::discriminant).collect::<Vec<_>>(),
            "Policy evaluation completed"
        );

        commands
    }
}
