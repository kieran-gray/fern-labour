use std::fmt::Debug;

use chrono::{DateTime, Duration, Utc};
use fern_labour_labour_shared::value_objects::{
    LabourPhase, LabourUpdateType, subscriber::status::SubscriberStatus,
};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use fern_labour_event_sourcing_rs::Aggregate;

use crate::durable_object::write_side::domain::{
    LabourCommand, LabourError, LabourEvent,
    entities::{
        contraction::Contraction,
        labour_update::{ANNOUNCEMENT_COOLDOWN_SECONDS, LabourUpdate},
        subscription::Subscription,
    },
    events::{
        ContractionDeleted, ContractionEnded, ContractionStarted, ContractionUpdated, LabourBegun,
        LabourCompleted, LabourDeleted, LabourInviteSent, LabourPlanUpdated, LabourPlanned,
        LabourUpdateDeleted, LabourUpdateMessageUpdated, LabourUpdatePosted,
        LabourUpdateTypeUpdated, SubscriberAccessLevelUpdated, SubscriberApproved,
        SubscriberBlocked, SubscriberNotificationMethodsUpdated, SubscriberRemoved,
        SubscriberRequested, SubscriberRoleUpdated, SubscriberUnblocked, SubscriberUnsubscribed,
        SubscriptionTokenSet,
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

    pub fn subscriptions(&self) -> &[Subscription] {
        &self.subscriptions
    }

    pub fn subscription_token(&self) -> Option<&String> {
        self.subscription_token.as_ref()
    }

    fn find_active_contraction(&self) -> Option<&Contraction> {
        self.contractions.iter().find(|c| c.is_active())
    }

    fn find_contraction(&self, contraction_id: Uuid) -> Option<&Contraction> {
        self.contractions.iter().find(|c| c.id() == contraction_id)
    }

    fn find_labour_update(&self, labour_update_id: Uuid) -> Option<&LabourUpdate> {
        self.labour_updates
            .iter()
            .find(|lu| lu.id() == labour_update_id)
    }

    fn find_last_announcement(&self) -> Option<&LabourUpdate> {
        self.labour_updates
            .iter()
            .filter(|lu| lu.labour_update_type() == &LabourUpdateType::ANNOUNCEMENT)
            .max_by_key(|lu| lu.sent_time())
    }

    fn can_send_announcement(&self) -> bool {
        match self.find_last_announcement() {
            None => true,
            Some(last) => {
                Utc::now() - last.sent_time() > Duration::seconds(ANNOUNCEMENT_COOLDOWN_SECONDS)
            }
        }
    }

    fn find_subscription_from_subscriber_id(&self, subscriber_id: &str) -> Option<&Subscription> {
        self.subscriptions
            .iter()
            .find(|s| s.subscriber_id() == subscriber_id)
    }

    fn find_subscription(&self, subscription_id: Uuid) -> Option<&Subscription> {
        self.subscriptions
            .iter()
            .find(|s| s.id() == subscription_id)
    }

    fn has_overlapping_contractions(
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
        let events = match command {
            LabourCommand::PlanLabour {
                labour_id,
                mother_id,
                first_labour,
                due_date,
                labour_name,
                mother_name,
            } => {
                if let Some(labour) = state {
                    return Err(LabourError::InvalidStateTransition(
                        labour.phase.to_string(),
                        LabourPhase::PLANNED.to_string(),
                    ));
                }

                vec![LabourEvent::LabourPlanned(LabourPlanned {
                    labour_id,
                    mother_id,
                    mother_name,
                    first_labour,
                    due_date,
                    labour_name,
                })]
            }
            LabourCommand::UpdateLabourPlan {
                labour_id,
                first_labour,
                due_date,
                labour_name,
            } => {
                if state.is_none() {
                    return Err(LabourError::NotFound);
                };

                vec![LabourEvent::LabourPlanUpdated(LabourPlanUpdated {
                    labour_id,
                    first_labour,
                    due_date,
                    labour_name,
                })]
            }
            LabourCommand::BeginLabour { labour_id } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase != LabourPhase::PLANNED {
                    return Err(LabourError::InvalidStateTransition(
                        labour.phase.to_string(),
                        LabourPhase::EARLY.to_string(),
                    ));
                }
                vec![LabourEvent::LabourBegun(LabourBegun {
                    labour_id,
                    start_time: Utc::now(),
                })]
            }
            LabourCommand::CompleteLabour { labour_id, notes } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase == LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidStateTransition(
                        labour.phase.to_string(),
                        LabourPhase::COMPLETE.to_string(),
                    ));
                }

                if labour.find_active_contraction().is_some() {
                    return Err(LabourError::ValidationError(
                        "Cannot complete labour with active contraction".to_string(),
                    ));
                }

                vec![LabourEvent::LabourCompleted(LabourCompleted {
                    labour_id,
                    notes,
                    end_time: Utc::now(),
                })]
            }
            LabourCommand::SendLabourInvite {
                labour_id,
                invite_email,
            } => {
                // TODO rate limiting checks per invite_email
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase == LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidCommand(
                        "Cannot invite to completed labour".to_string(),
                    ));
                }

                vec![LabourEvent::LabourInviteSent(LabourInviteSent {
                    labour_id,
                    invite_email,
                })]
            }
            LabourCommand::DeleteLabour { labour_id } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase != LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidCommand(
                        "Cannot delete active labour".to_string(),
                    ));
                }

                vec![LabourEvent::LabourDeleted(LabourDeleted { labour_id })]
            }
            LabourCommand::StartContraction {
                labour_id,
                start_time,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase == LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidCommand(
                        "Cannot start contraction in completed labour".to_string(),
                    ));
                }

                if labour.find_active_contraction().is_some() {
                    return Err(LabourError::InvalidCommand(
                        "Labour already has a contraction in progress".to_string(),
                    ));
                }

                let mut events = vec![];

                if labour.phase == LabourPhase::PLANNED {
                    events.push(LabourEvent::LabourBegun(LabourBegun {
                        labour_id,
                        start_time: Utc::now(),
                    }));
                    events.push(LabourEvent::LabourUpdatePosted(LabourUpdatePosted {
                        labour_id,
                        labour_update_id: Uuid::now_v7(),
                        labour_update_type: LabourUpdateType::PRIVATE_NOTE,
                        message: "labour_begun".to_string(),
                        application_generated: true,
                        sent_time: Utc::now(),
                    }))
                }

                events.push(LabourEvent::ContractionStarted(ContractionStarted {
                    labour_id,
                    contraction_id: Uuid::now_v7(),
                    start_time,
                }));

                events
            }
            LabourCommand::EndContraction {
                labour_id,
                end_time,
                intensity,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase == LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidCommand(
                        "Cannot start contraction in completed labour".to_string(),
                    ));
                }

                match labour.find_active_contraction() {
                    Some(contraction) => vec![LabourEvent::ContractionEnded(ContractionEnded {
                        labour_id,
                        contraction_id: contraction.id(),
                        end_time,
                        intensity,
                    })],
                    None => {
                        return Err(LabourError::InvalidCommand(
                            "Labour does not have an active contraction".to_string(),
                        ));
                    }
                }
            }
            LabourCommand::UpdateContraction {
                labour_id,
                contraction_id,
                start_time,
                end_time,
                intensity,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase == LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidCommand(
                        "Cannot update contraction in completed labour".to_string(),
                    ));
                }

                let Some(contraction) = labour.find_contraction(contraction_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Contraction not found".to_string(),
                    ));
                };

                if contraction.is_active() {
                    return Err(LabourError::InvalidCommand(
                        "Cannot update active contraction".to_string(),
                    ));
                }

                if (start_time.is_some() || end_time.is_some())
                    && labour.has_overlapping_contractions(contraction_id, start_time, end_time)
                {
                    return Err(LabourError::ValidationError(
                        "Updated contraction would overlap with existing contractions".to_string(),
                    ));
                }

                vec![LabourEvent::ContractionUpdated(ContractionUpdated {
                    labour_id,
                    contraction_id,
                    start_time,
                    end_time,
                    intensity,
                })]
            }
            LabourCommand::DeleteContraction {
                labour_id,
                contraction_id,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.phase == LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidCommand(
                        "Cannot delete contraction in completed labour".to_string(),
                    ));
                }

                let Some(contraction) = labour.find_contraction(contraction_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Contraction not found".to_string(),
                    ));
                };

                if contraction.is_active() {
                    return Err(LabourError::InvalidCommand(
                        "Cannot delete active contraction".to_string(),
                    ));
                }

                vec![LabourEvent::ContractionDeleted(ContractionDeleted {
                    labour_id,
                    contraction_id,
                })]
            }
            LabourCommand::PostLabourUpdate {
                labour_id,
                labour_update_type,
                message,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour_update_type == LabourUpdateType::ANNOUNCEMENT
                    && !labour.can_send_announcement()
                {
                    return Err(LabourError::InvalidCommand(
                        "Too soon since last announcement".to_string(),
                    ));
                }

                vec![LabourEvent::LabourUpdatePosted(LabourUpdatePosted {
                    labour_id,
                    labour_update_id: Uuid::now_v7(),
                    labour_update_type,
                    message,
                    application_generated: false,
                    sent_time: Utc::now(),
                })]
            }
            LabourCommand::PostApplicationLabourUpdate { labour_id, message } => {
                if state.is_none() {
                    return Err(LabourError::NotFound);
                };

                vec![LabourEvent::LabourUpdatePosted(LabourUpdatePosted {
                    labour_id,
                    labour_update_id: Uuid::now_v7(),
                    labour_update_type: LabourUpdateType::PRIVATE_NOTE,
                    message,
                    application_generated: true,
                    sent_time: Utc::now(),
                })]
            }
            LabourCommand::UpdateLabourUpdateType {
                labour_id,
                labour_update_id,
                labour_update_type,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(labour_update) = labour.find_labour_update(labour_update_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Labour update not found".to_string(),
                    ));
                };

                if labour_update.labour_update_type() == &LabourUpdateType::ANNOUNCEMENT {
                    return Err(LabourError::InvalidCommand(
                        "Cannot update an announcement".to_string(),
                    ));
                }

                if labour_update_type == LabourUpdateType::ANNOUNCEMENT
                    && !labour.can_send_announcement()
                {
                    return Err(LabourError::InvalidCommand(
                        "Too soon since last announcement".to_string(),
                    ));
                }

                vec![LabourEvent::LabourUpdateTypeUpdated(
                    LabourUpdateTypeUpdated {
                        labour_id,
                        labour_update_id,
                        labour_update_type,
                    },
                )]
            }
            LabourCommand::UpdateLabourUpdateMessage {
                labour_id,
                labour_update_id,
                message,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(labour_update) = labour.find_labour_update(labour_update_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Labour update not found".to_string(),
                    ));
                };

                if labour_update.labour_update_type() == &LabourUpdateType::ANNOUNCEMENT {
                    return Err(LabourError::InvalidCommand(
                        "Cannot update an announcement".to_string(),
                    ));
                }

                vec![LabourEvent::LabourUpdateMessageUpdated(
                    LabourUpdateMessageUpdated {
                        labour_id,
                        labour_update_id,
                        message,
                    },
                )]
            }
            LabourCommand::DeleteLabourUpdate {
                labour_id,
                labour_update_id,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(_) = labour.find_labour_update(labour_update_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Labour update not found".to_string(),
                    ));
                };

                vec![LabourEvent::LabourUpdateDeleted(LabourUpdateDeleted {
                    labour_id,
                    labour_update_id,
                })]
            }
            LabourCommand::SetSubscriptionToken {
                labour_id,
                mother_id,
                token,
            } => {
                let Some(_) = state else {
                    return Err(LabourError::NotFound);
                };
                vec![LabourEvent::SubscriptionTokenSet(SubscriptionTokenSet {
                    labour_id,
                    mother_id,
                    token,
                })]
            }
            LabourCommand::RequestAccess {
                labour_id,
                subscriber_id,
                token,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if subscriber_id == labour.mother_id {
                    return Err(LabourError::InvalidCommand(
                        "Cannot subscribe to own labour".to_string(),
                    ));
                }

                if labour.phase == LabourPhase::COMPLETE {
                    return Err(LabourError::InvalidCommand(
                        "Cannot subscribe to completed labour".to_string(),
                    ));
                }

                let Some(ref subscription_token) = labour.subscription_token else {
                    return Err(LabourError::InvalidCommand(
                        "Labour has no subscription token set".to_string(),
                    ));
                };

                if &token != subscription_token {
                    return Err(LabourError::InvalidCommand(
                        "Incorrect subscription token".to_string(),
                    ));
                }

                let mut events = vec![];

                if let Some(subscription) =
                    labour.find_subscription_from_subscriber_id(&subscriber_id)
                {
                    if [
                        SubscriberStatus::BLOCKED,
                        SubscriberStatus::SUBSCRIBED,
                        SubscriberStatus::REQUESTED,
                    ]
                    .contains(subscription.status())
                    {
                        return Err(LabourError::InvalidCommand(
                            "Cannot subscribe to labour".to_string(),
                        ));
                    }
                    events.push(LabourEvent::SubscriberRequested(SubscriberRequested {
                        labour_id,
                        subscriber_id,
                        subscription_id: subscription.id(),
                    }))
                } else {
                    events.push(LabourEvent::SubscriberRequested(SubscriberRequested {
                        labour_id,
                        subscriber_id,
                        subscription_id: Uuid::now_v7(),
                    }))
                }
                events
            }
            LabourCommand::Unsubscribe {
                labour_id,
                subscription_id,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(subscription) = labour.find_subscription(subscription_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                if subscription.status() != &SubscriberStatus::SUBSCRIBED {
                    return Err(LabourError::InvalidCommand(
                        "Cannot unsubscribe from labour".to_string(),
                    ));
                }

                vec![LabourEvent::SubscriberUnsubscribed(
                    SubscriberUnsubscribed {
                        labour_id,
                        subscription_id,
                    },
                )]
            }
            LabourCommand::UpdateNotificationMethods {
                labour_id,
                subscription_id,
                notification_methods,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                if labour.find_subscription(subscription_id).is_none() {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                vec![LabourEvent::SubscriberNotificationMethodsUpdated(
                    SubscriberNotificationMethodsUpdated {
                        labour_id,
                        subscription_id,
                        notification_methods,
                    },
                )]
            }
            LabourCommand::UpdateAccessLevel {
                labour_id,
                subscription_id,
                access_level,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(subscription) = labour.find_subscription(subscription_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                if subscription.access_level() == &access_level {
                    return Err(LabourError::InvalidCommand(
                        "Subscription already has access level".to_string(),
                    ));
                }

                vec![LabourEvent::SubscriberAccessLevelUpdated(
                    SubscriberAccessLevelUpdated {
                        labour_id,
                        subscription_id,
                        access_level,
                    },
                )]
            }
            LabourCommand::ApproveSubscriber {
                labour_id,
                subscription_id,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(subscription) = labour.find_subscription(subscription_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                if subscription.status() != &SubscriberStatus::REQUESTED {
                    return Err(LabourError::InvalidCommand(
                        "Subscription is not in REQUESTED state".to_string(),
                    ));
                }

                vec![LabourEvent::SubscriberApproved(SubscriberApproved {
                    labour_id,
                    subscription_id,
                })]
            }
            LabourCommand::RemoveSubscriber {
                labour_id,
                subscription_id,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(subscription) = labour.find_subscription(subscription_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                if [SubscriberStatus::BLOCKED, SubscriberStatus::REMOVED]
                    .contains(subscription.status())
                {
                    return Err(LabourError::InvalidCommand(
                        "Cannot remove subscriber".to_string(),
                    ));
                }

                vec![LabourEvent::SubscriberRemoved(SubscriberRemoved {
                    labour_id,
                    subscription_id,
                })]
            }
            LabourCommand::BlockSubscriber {
                labour_id,
                subscription_id,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(subscription) = labour.find_subscription(subscription_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                if subscription.status() == &SubscriberStatus::BLOCKED {
                    return Err(LabourError::InvalidCommand(
                        "Subscriber is already blocked".to_string(),
                    ));
                }

                vec![LabourEvent::SubscriberBlocked(SubscriberBlocked {
                    labour_id,
                    subscription_id,
                })]
            }
            LabourCommand::UnblockSubscriber {
                labour_id,
                subscription_id,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(subscription) = labour.find_subscription(subscription_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                if subscription.status() != &SubscriberStatus::BLOCKED {
                    return Err(LabourError::InvalidCommand(
                        "Subscriber is not blocked".to_string(),
                    ));
                }

                vec![LabourEvent::SubscriberUnblocked(SubscriberUnblocked {
                    labour_id,
                    subscription_id,
                })]
            }
            LabourCommand::UpdateSubscriberRole {
                labour_id,
                subscription_id,
                role,
            } => {
                let Some(labour) = state else {
                    return Err(LabourError::NotFound);
                };

                let Some(subscription) = labour.find_subscription(subscription_id) else {
                    return Err(LabourError::InvalidCommand(
                        "Subscription not found".to_string(),
                    ));
                };

                if &role == subscription.role() {
                    return Err(LabourError::InvalidCommand(
                        "Subscriber already has role".to_string(),
                    ));
                }

                vec![LabourEvent::SubscriberRoleUpdated(SubscriberRoleUpdated {
                    labour_id,
                    subscription_id,
                    role,
                })]
            }
        };
        Ok(events)
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
