use chrono::Utc;
use fern_labour_labour_shared::value_objects::LabourPhase;
use uuid::Uuid;

use crate::durable_object::write_side::domain::{
    Labour, LabourError, LabourEvent,
    commands::contraction::{
        DeleteContraction, EndContraction, StartContraction, UpdateContraction,
    },
    events::{
        ContractionDeleted, ContractionEnded, ContractionStarted, ContractionUpdated, LabourBegun,
    },
};

pub fn handle_start_contraction(
    state: Option<&Labour>,
    cmd: StartContraction,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let current_phase = labour.phase();

    if current_phase == &LabourPhase::COMPLETE {
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

    if current_phase == &LabourPhase::PLANNED {
        events.push(LabourEvent::LabourBegun(LabourBegun {
            labour_id: cmd.labour_id,
            start_time: Utc::now(),
        }));
    }

    events.push(LabourEvent::ContractionStarted(ContractionStarted {
        labour_id: cmd.labour_id,
        contraction_id: Uuid::now_v7(),
        start_time: cmd.start_time,
    }));

    Ok(events)
}

pub fn handle_end_contraction(
    state: Option<&Labour>,
    cmd: EndContraction,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    if labour.phase() == &LabourPhase::COMPLETE {
        return Err(LabourError::InvalidCommand(
            "Cannot start contraction in completed labour".to_string(),
        ));
    }

    match labour.find_active_contraction() {
        Some(contraction) => Ok(vec![LabourEvent::ContractionEnded(ContractionEnded {
            labour_id: cmd.labour_id,
            contraction_id: contraction.id(),
            end_time: cmd.end_time,
            intensity: cmd.intensity,
        })]),
        None => Err(LabourError::InvalidCommand(
            "Labour does not have an active contraction".to_string(),
        )),
    }
}

pub fn handle_update_contraction(
    state: Option<&Labour>,
    cmd: UpdateContraction,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    if labour.phase() == &LabourPhase::COMPLETE {
        return Err(LabourError::InvalidCommand(
            "Cannot update contraction in completed labour".to_string(),
        ));
    }

    let Some(contraction) = labour.find_contraction(cmd.contraction_id) else {
        return Err(LabourError::InvalidCommand(
            "Contraction not found".to_string(),
        ));
    };

    if contraction.is_active() {
        return Err(LabourError::InvalidCommand(
            "Cannot update active contraction".to_string(),
        ));
    }

    if (cmd.start_time.is_some() || cmd.end_time.is_some())
        && labour.has_overlapping_contractions(cmd.contraction_id, cmd.start_time, cmd.end_time)
    {
        return Err(LabourError::ValidationError(
            "Updated contraction would overlap with existing contractions".to_string(),
        ));
    }

    Ok(vec![LabourEvent::ContractionUpdated(ContractionUpdated {
        labour_id: cmd.labour_id,
        contraction_id: cmd.contraction_id,
        start_time: cmd.start_time,
        end_time: cmd.end_time,
        intensity: cmd.intensity,
    })])
}

pub fn handle_delete_contraction(
    state: Option<&Labour>,
    cmd: DeleteContraction,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    if labour.phase() == &LabourPhase::COMPLETE {
        return Err(LabourError::InvalidCommand(
            "Cannot delete contraction in completed labour".to_string(),
        ));
    }

    let Some(contraction) = labour.find_contraction(cmd.contraction_id) else {
        return Err(LabourError::InvalidCommand(
            "Contraction not found".to_string(),
        ));
    };

    if contraction.is_active() {
        return Err(LabourError::InvalidCommand(
            "Cannot delete active contraction".to_string(),
        ));
    }

    Ok(vec![LabourEvent::ContractionDeleted(ContractionDeleted {
        labour_id: cmd.labour_id,
        contraction_id: cmd.contraction_id,
    })])
}
