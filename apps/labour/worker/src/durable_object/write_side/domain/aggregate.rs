use std::fmt::Debug;

use chrono::{DateTime, Duration, Utc};
use fern_labour_labour_shared::value_objects::{LabourPhase, LabourUpdateType};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use fern_labour_event_sourcing_rs::Aggregate;

use crate::durable_object::write_side::domain::{
    LabourCommand, LabourError, LabourEvent,
    entities::{contraction::Contraction, labour_update::LabourUpdate},
};

// TODO move somewhere else
const ANNOUNCEMENT_COOLDOWN_SECONDS: i64 = 10;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Labour {
    id: Uuid,
    birthing_person_id: String,
    phase: LabourPhase,
    contractions: Vec<Contraction>,
    labour_updates: Vec<LabourUpdate>,
    start_time: Option<DateTime<Utc>>,
    end_time: Option<DateTime<Utc>>,
}

impl Labour {
    // TODO which need to be public
    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn birthing_person_id(&self) -> &String {
        &self.birthing_person_id
    }

    pub fn phase(&self) -> &LabourPhase {
        &self.phase
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
            LabourEvent::LabourPlanned {
                labour_id,
                birthing_person_id,
                ..
            } => {
                self.id = *labour_id;
                self.birthing_person_id = birthing_person_id.clone();
                self.phase = LabourPhase::PLANNED;
            }
            LabourEvent::LabourBegun { start_time, .. } => {
                self.start_time = Some(*start_time);
                self.phase = LabourPhase::EARLY;
            }
            LabourEvent::LabourCompleted { end_time, .. } => {
                self.end_time = Some(*end_time);
                self.phase = LabourPhase::COMPLETE;
            }
            LabourEvent::ContractionStarted {
                labour_id,
                contraction_id,
                start_time,
            } => {
                let contraction =
                    Contraction::start(*contraction_id, *labour_id, *start_time).unwrap();
                self.contractions.push(contraction);
            }
            LabourEvent::ContractionEnded {
                end_time,
                intensity,
                ..
            } => {
                let contraction = self.contractions.last_mut().expect("No contractions found");
                contraction.end(*end_time, *intensity).unwrap();
            }
            LabourEvent::ContractionUpdated { .. } => {
                // TODO: skip CBA for now
            }
            LabourEvent::ContractionDeleted { contraction_id, .. } => {
                self.contractions.pop_if(|c| c.id() == *contraction_id);
            }
            LabourEvent::LabourUpdatePosted {
                labour_id,
                labour_update_id,
                labour_update_type,
                message,
                application_generated,
                sent_time,
            } => {
                let labour_update = LabourUpdate::create(
                    *labour_id,
                    *labour_update_id,
                    labour_update_type.clone(),
                    message.clone(),
                    *sent_time,
                    *application_generated,
                );
                self.labour_updates.push(labour_update);
            }
            LabourEvent::LabourUpdateMessageUpdated { .. } => {
                // TODO
            }
            LabourEvent::LabourUpdateTypeUpdated { .. } => {
                // TODO
            }
            LabourEvent::LabourUpdateDeleted {
                labour_update_id, ..
            } => {
                self.labour_updates.pop_if(|c| c.id() == *labour_update_id);
            }
            LabourEvent::LabourPlanUpdated { .. }
            | LabourEvent::LabourInviteSent { .. }
            | LabourEvent::LabourDeleted { .. } => {}
        }
    }

    fn handle_command(
        state: Option<&Self>,
        command: Self::Command,
    ) -> std::result::Result<Vec<Self::Event>, Self::Error> {
        let events = match command {
            LabourCommand::PlanLabour {
                labour_id,
                birthing_person_id,
                first_labour,
                due_date,
                labour_name,
            } => {
                if let Some(labour) = state {
                    return Err(LabourError::InvalidStateTransition(
                        labour.phase.to_string(),
                        LabourPhase::PLANNED.to_string(),
                    ));
                }

                vec![LabourEvent::LabourPlanned {
                    labour_id,
                    birthing_person_id,
                    first_labour,
                    due_date,
                    labour_name,
                }]
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

                vec![LabourEvent::LabourPlanUpdated {
                    labour_id,
                    first_labour,
                    due_date,
                    labour_name,
                }]
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
                // TODO: labour update would be better as a policy?
                vec![
                    LabourEvent::LabourBegun {
                        labour_id,
                        start_time: Utc::now(),
                    },
                    LabourEvent::LabourUpdatePosted {
                        labour_id,
                        labour_update_id: Uuid::now_v7(),
                        labour_update_type: LabourUpdateType::PRIVATE_NOTE,
                        message: "labour_begun".to_string(),
                        application_generated: true,
                        sent_time: Utc::now(),
                    },
                ]
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

                vec![LabourEvent::LabourCompleted {
                    labour_id,
                    notes,
                    end_time: Utc::now(),
                }]
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

                vec![LabourEvent::LabourInviteSent {
                    labour_id,
                    invite_email,
                }]
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

                vec![LabourEvent::LabourDeleted { labour_id }]
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
                    events.push(LabourEvent::LabourBegun {
                        labour_id,
                        start_time: Utc::now(),
                    });
                    events.push(LabourEvent::LabourUpdatePosted {
                        labour_id,
                        labour_update_id: Uuid::now_v7(),
                        labour_update_type: LabourUpdateType::PRIVATE_NOTE,
                        message: "labour_begun".to_string(),
                        application_generated: true,
                        sent_time: Utc::now(),
                    })
                }

                events.push(LabourEvent::ContractionStarted {
                    labour_id,
                    contraction_id: Uuid::now_v7(),
                    start_time,
                });

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
                    Some(contraction) => vec![LabourEvent::ContractionEnded {
                        labour_id,
                        contraction_id: contraction.id(),
                        end_time,
                        intensity,
                    }],
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

                // TODO actual update validation logic to check for overlapping contractions etc.

                vec![LabourEvent::ContractionUpdated {
                    labour_id,
                    contraction_id,
                    start_time,
                    end_time,
                    intensity,
                }]
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

                vec![LabourEvent::ContractionDeleted {
                    labour_id,
                    contraction_id,
                }]
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

                vec![LabourEvent::LabourUpdatePosted {
                    labour_id,
                    labour_update_id: Uuid::now_v7(),
                    labour_update_type,
                    message,
                    application_generated: false,
                    sent_time: Utc::now(),
                }]
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

                vec![LabourEvent::LabourUpdateTypeUpdated {
                    labour_id,
                    labour_update_id,
                    labour_update_type,
                }]
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

                vec![LabourEvent::LabourUpdateMessageUpdated {
                    labour_id,
                    labour_update_id,
                    message,
                }]
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

                vec![LabourEvent::LabourUpdateDeleted {
                    labour_id,
                    labour_update_id,
                }]
            }
        };
        Ok(events)
    }

    fn from_events(events: &[Self::Event]) -> Option<Self> {
        let mut notification = match events.first() {
            Some(LabourEvent::LabourPlanned {
                labour_id,
                birthing_person_id,
                ..
            }) => Labour {
                id: *labour_id,
                birthing_person_id: birthing_person_id.clone(),
                phase: LabourPhase::PLANNED,
                contractions: vec![],
                labour_updates: vec![],
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
