use std::fmt::Debug;

use chrono::{DateTime, Duration, Utc};
use fern_labour_labour_shared::value_objects::{LabourPhase, LabourUpdateType};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use fern_labour_event_sourcing_rs::Aggregate;

use crate::durable_object::write_side::domain::{
    LabourCommand, LabourError, LabourEvent,
    command_handlers::*,
    entities::{
        contraction::Contraction,
        labour_update::{ANNOUNCEMENT_COOLDOWN_SECONDS, LabourUpdate},
        subscription::Subscription,
    },
};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Labour {
    id: Uuid,
    mother_id: String,
    phase: LabourPhase,
    subscription_token: Option<String>,
    contractions: Vec<Contraction>,
    labour_updates: Vec<LabourUpdate>,
    subscriptions: Vec<Subscription>,
    start_time: Option<DateTime<Utc>>,
    end_time: Option<DateTime<Utc>>,
}

impl Labour {
    pub fn mother_id(&self) -> &str {
        &self.mother_id
    }

    pub fn phase(&self) -> &LabourPhase {
        &self.phase
    }

    pub fn subscriptions(&self) -> &[Subscription] {
        &self.subscriptions
    }

    pub fn subscription_token(&self) -> Option<&String> {
        self.subscription_token.as_ref()
    }

    pub fn find_active_contraction(&self) -> Option<&Contraction> {
        self.contractions.iter().find(|c| c.is_active())
    }

    pub fn find_contraction(&self, contraction_id: Uuid) -> Option<&Contraction> {
        self.contractions.iter().find(|c| c.id() == contraction_id)
    }

    pub fn find_labour_update(&self, labour_update_id: Uuid) -> Option<&LabourUpdate> {
        self.labour_updates
            .iter()
            .find(|lu| lu.id() == labour_update_id)
    }

    pub fn find_last_announcement(&self) -> Option<&LabourUpdate> {
        self.labour_updates
            .iter()
            .filter(|lu| lu.labour_update_type() == &LabourUpdateType::ANNOUNCEMENT)
            .max_by_key(|lu| lu.sent_time())
    }

    pub fn can_send_announcement(&self) -> bool {
        match self.find_last_announcement() {
            None => true,
            Some(last) => {
                Utc::now() - last.sent_time() > Duration::seconds(ANNOUNCEMENT_COOLDOWN_SECONDS)
            }
        }
    }

    pub fn find_subscription_from_subscriber_id(
        &self,
        subscriber_id: &str,
    ) -> Option<&Subscription> {
        self.subscriptions
            .iter()
            .find(|s| s.subscriber_id() == subscriber_id)
    }

    pub fn find_subscription(&self, subscription_id: Uuid) -> Option<&Subscription> {
        self.subscriptions
            .iter()
            .find(|s| s.id() == subscription_id)
    }

    pub fn has_overlapping_contractions(
        &self,
        updated_contraction_id: Uuid,
        start_time: Option<DateTime<Utc>>,
        end_time: Option<DateTime<Utc>>,
    ) -> bool {
        if self.contractions.len() <= 1 {
            return false;
        }

        let updated_contraction = match self.find_contraction(updated_contraction_id) {
            Some(c) => c,
            None => return false,
        };

        let new_start = start_time.unwrap_or(*updated_contraction.start_time());
        let new_end = end_time.unwrap_or(*updated_contraction.end_time());

        for contraction in &self.contractions {
            if contraction.id() == updated_contraction_id || contraction.is_active() {
                continue;
            }

            if new_start < *contraction.end_time() && *contraction.start_time() < new_end {
                return true;
            }
        }

        false
    }
}

impl Aggregate for Labour {
    type Command = LabourCommand;
    type Error = LabourError;
    type Event = LabourEvent;

    fn aggregate_id(&self) -> String {
        self.id.to_string()
    }

    fn apply(&mut self, event: &Self::Event) {
        match event {
            LabourEvent::LabourPlanned(e) => {
                self.id = e.labour_id;
                self.mother_id = e.mother_id.clone();
                self.phase = LabourPhase::PLANNED;
            }
            LabourEvent::LabourBegun(e) => {
                self.start_time = Some(e.start_time);
                self.phase = LabourPhase::EARLY;
            }
            LabourEvent::LabourCompleted(e) => {
                self.end_time = Some(e.end_time);
                self.phase = LabourPhase::COMPLETE;
            }
            LabourEvent::ContractionStarted(e) => {
                if let Ok(contraction) =
                    Contraction::start(e.contraction_id, e.labour_id, e.start_time)
                {
                    self.contractions.push(contraction);
                }
            }
            LabourEvent::ContractionEnded(e) => {
                if let Some(contraction) = self.contractions.last_mut() {
                    contraction
                        .end(e.end_time, e.intensity)
                        .expect("Failed to end contraction");
                }
            }
            LabourEvent::ContractionUpdated(e) => {
                if let Some(contraction) = self
                    .contractions
                    .iter_mut()
                    .find(|c| c.id() == e.contraction_id)
                {
                    contraction
                        .update(e.start_time, e.end_time, e.intensity)
                        .expect("Failed to update contraction");
                }
            }
            LabourEvent::ContractionDeleted(e) => {
                self.contractions.pop_if(|c| c.id() == e.contraction_id);
            }
            LabourEvent::LabourUpdatePosted(e) => {
                let labour_update = LabourUpdate::create(
                    e.labour_id,
                    e.labour_update_id,
                    e.labour_update_type.clone(),
                    e.message.clone(),
                    e.sent_time,
                    e.application_generated,
                );
                self.labour_updates.push(labour_update);
            }
            LabourEvent::LabourUpdateMessageUpdated(e) => {
                if let Some(labour_update) = self
                    .labour_updates
                    .iter_mut()
                    .find(|lu| lu.id() == e.labour_update_id)
                {
                    labour_update.update_message(e.message.clone());
                }
            }
            LabourEvent::LabourUpdateTypeUpdated(e) => {
                if let Some(labour_update) = self
                    .labour_updates
                    .iter_mut()
                    .find(|lu| lu.id() == e.labour_update_id)
                {
                    labour_update.update_type(e.labour_update_type.clone());
                }
            }
            LabourEvent::LabourUpdateDeleted(e) => {
                self.labour_updates.pop_if(|c| c.id() == e.labour_update_id);
            }
            LabourEvent::SubscriberRequested(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.request();
                } else {
                    let subscription = Subscription::create(
                        e.subscription_id,
                        e.labour_id,
                        e.subscriber_id.clone(),
                    );
                    self.subscriptions.push(subscription);
                }
            }
            LabourEvent::SubscriberUnsubscribed(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.unsubscribe();
                }
            }
            LabourEvent::SubscriberNotificationMethodsUpdated(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.update_notification_methods(e.notification_methods.clone());
                }
            }
            LabourEvent::SubscriberAccessLevelUpdated(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.update_access_level(e.access_level.clone());
                }
            }
            LabourEvent::SubscriberApproved(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.approve();
                }
            }
            LabourEvent::SubscriberRemoved(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.remove();
                }
            }
            LabourEvent::SubscriberBlocked(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.block();
                }
            }
            LabourEvent::SubscriberUnblocked(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.unblock();
                }
            }
            LabourEvent::SubscriberRoleUpdated(e) => {
                if let Some(subscription) = self
                    .subscriptions
                    .iter_mut()
                    .find(|s| s.id() == e.subscription_id)
                {
                    subscription.update_role(e.role.clone());
                }
            }
            LabourEvent::SubscriptionTokenSet(e) => {
                self.subscription_token = Some(e.token.clone());
            }
            LabourEvent::LabourPlanUpdated(_)
            | LabourEvent::LabourInviteSent(_)
            | LabourEvent::LabourDeleted(_) => {}
        }
    }

    fn handle_command(
        state: Option<&Self>,
        command: Self::Command,
    ) -> std::result::Result<Vec<Self::Event>, Self::Error> {
        match command {
            // Labour commands
            LabourCommand::PlanLabour(cmd) => handle_plan_labour(state, cmd),
            LabourCommand::UpdateLabourPlan(cmd) => handle_update_labour_plan(state, cmd),
            LabourCommand::BeginLabour(cmd) => handle_begin_labour(state, cmd),
            LabourCommand::CompleteLabour(cmd) => handle_complete_labour(state, cmd),
            LabourCommand::SendLabourInvite(cmd) => handle_send_labour_invite(state, cmd),
            LabourCommand::DeleteLabour(cmd) => handle_delete_labour(state, cmd),

            // Contraction commands
            LabourCommand::StartContraction(cmd) => handle_start_contraction(state, cmd),
            LabourCommand::EndContraction(cmd) => handle_end_contraction(state, cmd),
            LabourCommand::UpdateContraction(cmd) => handle_update_contraction(state, cmd),
            LabourCommand::DeleteContraction(cmd) => handle_delete_contraction(state, cmd),

            // Labour update commands
            LabourCommand::PostLabourUpdate(cmd) => handle_post_labour_update(state, cmd),
            LabourCommand::PostApplicationLabourUpdate(cmd) => {
                handle_post_application_labour_update(state, cmd)
            }
            LabourCommand::UpdateLabourUpdateType(cmd) => {
                handle_update_labour_update_type(state, cmd)
            }
            LabourCommand::UpdateLabourUpdateMessage(cmd) => {
                handle_update_labour_update_message(state, cmd)
            }
            LabourCommand::DeleteLabourUpdate(cmd) => handle_delete_labour_update(state, cmd),

            // Subscriber commands
            LabourCommand::RequestAccess(cmd) => handle_request_access(state, cmd),
            LabourCommand::Unsubscribe(cmd) => handle_unsubscribe(state, cmd),
            LabourCommand::UpdateNotificationMethods(cmd) => {
                handle_update_notification_methods(state, cmd)
            }
            LabourCommand::UpdateAccessLevel(cmd) => handle_update_access_level(state, cmd),

            // Subscription commands
            LabourCommand::SetSubscriptionToken(cmd) => handle_set_subscription_token(state, cmd),
            LabourCommand::ApproveSubscriber(cmd) => handle_approve_subscriber(state, cmd),
            LabourCommand::RemoveSubscriber(cmd) => handle_remove_subscriber(state, cmd),
            LabourCommand::BlockSubscriber(cmd) => handle_block_subscriber(state, cmd),
            LabourCommand::UnblockSubscriber(cmd) => handle_unblock_subscriber(state, cmd),
            LabourCommand::UpdateSubscriberRole(cmd) => handle_update_subscriber_role(state, cmd),
        }
    }

    fn from_events(events: &[Self::Event]) -> Option<Self> {
        let mut notification = match events.first() {
            Some(LabourEvent::LabourPlanned(e)) => Labour {
                id: e.labour_id,
                mother_id: e.mother_id.clone(),
                phase: LabourPhase::PLANNED,
                subscription_token: None,
                contractions: vec![],
                labour_updates: vec![],
                subscriptions: vec![],
                start_time: None,
                end_time: None,
            },
            _ => return None,
        };

        for event in events.iter().skip(1) {
            notification.apply(event);
        }

        Some(notification)
    }
}
