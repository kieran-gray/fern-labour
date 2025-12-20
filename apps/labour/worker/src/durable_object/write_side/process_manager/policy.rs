use fern_labour_labour_shared::value_objects::{
    LabourUpdateType, SubscriberContactMethod, subscriber::status::SubscriberStatus,
};
use uuid::Uuid;

use crate::durable_object::write_side::{
    domain::{Labour, LabourEvent},
    process_manager::types::*,
};

pub trait EffectPolicy {
    type Event;
    type AggregateState;

    fn determine_effects(
        &self,
        event: &Self::Event,
        event_sequence: i64,
        aggregate_state: &Self::AggregateState,
    ) -> Vec<Effect>;
}

pub struct LabourEffectPolicy;

impl EffectPolicy for LabourEffectPolicy {
    type Event = LabourEvent;
    type AggregateState = Labour;

    fn determine_effects(&self, event: &LabourEvent, sequence: i64, state: &Labour) -> Vec<Effect> {
        match event {
            LabourEvent::LabourPlanned { labour_id, .. } => {
                self.generate_subscription_token(*labour_id, sequence, state)
            }
            LabourEvent::LabourBegun { labour_id, .. } => {
                self.notify_subscribers_of_labour_start(*labour_id, sequence, state)
            }
            LabourEvent::LabourCompleted {
                labour_id, notes, ..
            } => self.notify_subscribers_of_labour_complete(*labour_id, sequence, state, notes),
            LabourEvent::LabourUpdatePosted {
                labour_id,
                labour_update_type: LabourUpdateType::ANNOUNCEMENT,
                message,
                application_generated: false,
                ..
            } => self.notify_subscribers_of_announcement(*labour_id, sequence, state, message),
            LabourEvent::SubscriberApproved {
                labour_id,
                subscription_id,
                ..
            } => self.notify_subscriber_of_approval(*labour_id, sequence, *subscription_id, state),
            LabourEvent::SubscriberRequested {
                labour_id,
                subscriber_id,
                subscription_id,
                ..
            } => self.notify_mother_of_subscriber_request(
                *labour_id,
                sequence,
                subscriber_id,
                *subscription_id,
                state,
            ),
            LabourEvent::LabourInviteSent {
                labour_id,
                invite_email,
                ..
            } => self.send_labour_invite(*labour_id, sequence, invite_email, state),
            _ => vec![],
        }
    }
}

impl LabourEffectPolicy {
    fn generate_subscription_token(
        &self,
        labour_id: Uuid,
        sequence: i64,
        state: &Labour,
    ) -> Vec<Effect> {
        vec![Effect::GenerateSubscriptionToken {
            labour_id,
            mother_id: state.mother_id().to_string(),
            idempotency_key: IdempotencyKey::for_command(
                labour_id,
                sequence,
                "generate_subscription_token",
            ),
        }]
    }

    fn notify_subscribers_of_labour_start(
        &self,
        labour_id: Uuid,
        sequence: i64,
        state: &Labour,
    ) -> Vec<Effect> {
        let sender_id = state.mother_id().to_string();

        state
            .subscriptions()
            .iter()
            .filter(|s| s.status() == &SubscriberStatus::SUBSCRIBED)
            .flat_map(|subscription| {
                let sender_id = sender_id.clone();
                subscription.contact_methods().iter().map(move |channel| {
                    Effect::SendNotification(NotificationIntent {
                        idempotency_key: IdempotencyKey::for_notification(
                            labour_id,
                            sequence,
                            subscription.subscriber_id(),
                            "labour_started",
                        ),
                        context: NotificationContext::Subscriber {
                            recipient_user_id: subscription.subscriber_id().to_string(),
                            subscription_id: subscription.id(),
                            channel: channel.clone(),
                            sender_id: sender_id.clone(),
                            notification: SubscriberNotification::LabourStarted { labour_id },
                        },
                    })
                })
            })
            .collect()
    }

    fn notify_subscribers_of_labour_complete(
        &self,
        labour_id: Uuid,
        sequence: i64,
        state: &Labour,
        notes: &Option<String>,
    ) -> Vec<Effect> {
        let sender_id = state.mother_id().to_string();

        state
            .subscriptions()
            .iter()
            .filter(|s| s.status() == &SubscriberStatus::SUBSCRIBED)
            .flat_map(|subscription| {
                let sender_id = sender_id.clone();
                let notes = notes.clone();
                subscription.contact_methods().iter().map(move |channel| {
                    Effect::SendNotification(NotificationIntent {
                        idempotency_key: IdempotencyKey::for_notification(
                            labour_id,
                            sequence,
                            subscription.subscriber_id(),
                            "labour_completed",
                        ),
                        context: NotificationContext::Subscriber {
                            recipient_user_id: subscription.subscriber_id().to_string(),
                            subscription_id: subscription.id(),
                            channel: channel.clone(),
                            sender_id: sender_id.clone(),
                            notification: SubscriberNotification::LabourCompleted {
                                labour_id,
                                notes: notes.clone(),
                            },
                        },
                    })
                })
            })
            .collect()
    }

    fn notify_subscribers_of_announcement(
        &self,
        labour_id: Uuid,
        sequence: i64,
        state: &Labour,
        message: &str,
    ) -> Vec<Effect> {
        let sender_id = state.mother_id().to_string();

        state
            .subscriptions()
            .iter()
            .filter(|s| s.status() == &SubscriberStatus::SUBSCRIBED)
            .flat_map(|subscription| {
                let sender_id = sender_id.clone();
                let message = message.to_string();
                subscription.contact_methods().iter().map(move |channel| {
                    Effect::SendNotification(NotificationIntent {
                        idempotency_key: IdempotencyKey::for_notification(
                            labour_id,
                            sequence,
                            subscription.subscriber_id(),
                            "announcement",
                        ),
                        context: NotificationContext::Subscriber {
                            recipient_user_id: subscription.subscriber_id().to_string(),
                            subscription_id: subscription.id(),
                            channel: channel.clone(),
                            sender_id: sender_id.clone(),
                            notification: SubscriberNotification::AnnouncementPosted {
                                labour_id,
                                message: message.clone(),
                            },
                        },
                    })
                })
            })
            .collect()
    }

    fn notify_subscriber_of_approval(
        &self,
        labour_id: Uuid,
        sequence: i64,
        subscription_id: Uuid,
        state: &Labour,
    ) -> Vec<Effect> {
        let sender_id = state.mother_id().to_string();

        let subscription = state
            .subscriptions()
            .iter()
            .find(|s| s.id() == subscription_id);

        match subscription {
            Some(subscription) => {
                vec![Effect::SendNotification(NotificationIntent {
                    idempotency_key: IdempotencyKey::for_notification(
                        labour_id,
                        sequence,
                        subscription.subscriber_id(),
                        "approved",
                    ),
                    context: NotificationContext::Subscriber {
                        recipient_user_id: subscription.subscriber_id().to_string(),
                        subscription_id: subscription.id(),
                        channel: SubscriberContactMethod::EMAIL,
                        sender_id: sender_id.clone(),
                        notification: SubscriberNotification::SubscriptionApproved { labour_id },
                    },
                })]
            }
            None => vec![],
        }
    }

    fn notify_mother_of_subscriber_request(
        &self,
        labour_id: Uuid,
        sequence: i64,
        subscriber_id: &str,
        subscription_id: Uuid,
        state: &Labour,
    ) -> Vec<Effect> {
        let mother_id = state.mother_id().to_string();

        vec![Effect::SendNotification(NotificationIntent {
            idempotency_key: IdempotencyKey::for_notification(
                labour_id,
                sequence,
                &mother_id,
                "subscriber_requested",
            ),
            context: NotificationContext::LabourOwner {
                recipient_user_id: mother_id,
                channel: SubscriberContactMethod::EMAIL,
                notification: LabourOwnerNotification::SubscriberRequested {
                    labour_id,
                    subscription_id,
                    requester_user_id: subscriber_id.to_string(),
                },
            },
        })]
    }

    fn send_labour_invite(
        &self,
        labour_id: Uuid,
        sequence: i64,
        invite_email: &str,
        state: &Labour,
    ) -> Vec<Effect> {
        let sender_id = state.mother_id().to_string();

        vec![Effect::SendNotification(NotificationIntent {
            idempotency_key: IdempotencyKey::for_notification(
                labour_id,
                sequence,
                invite_email,
                "invite",
            ),
            context: NotificationContext::Email {
                email: invite_email.to_string(),
                sender_id,
                notification: EmailNotification::LabourInvite { labour_id },
            },
        })]
    }
}
