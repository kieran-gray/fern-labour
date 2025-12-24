use chrono::Utc;
use fern_labour_labour_shared::value_objects::LabourPhase;

use crate::durable_object::write_side::domain::{
    Labour, LabourError, LabourEvent,
    commands::labour::{
        BeginLabour, CompleteLabour, DeleteLabour, PlanLabour, SendLabourInvite, UpdateLabourPlan,
    },
    events::{
        LabourBegun, LabourCompleted, LabourDeleted, LabourInviteSent, LabourPlanUpdated,
        LabourPlanned,
    },
};

pub fn handle_plan_labour(
    state: Option<&Labour>,
    cmd: PlanLabour,
) -> Result<Vec<LabourEvent>, LabourError> {
    if let Some(labour) = state {
        return Err(LabourError::InvalidStateTransition(
            labour.phase().to_string(),
            LabourPhase::PLANNED.to_string(),
        ));
    }

    Ok(vec![LabourEvent::LabourPlanned(LabourPlanned {
        labour_id: cmd.labour_id,
        mother_id: cmd.mother_id,
        mother_name: cmd.mother_name,
        first_labour: cmd.first_labour,
        due_date: cmd.due_date,
        labour_name: cmd.labour_name,
    })])
}

pub fn handle_update_labour_plan(
    state: Option<&Labour>,
    cmd: UpdateLabourPlan,
) -> Result<Vec<LabourEvent>, LabourError> {
    if state.is_none() {
        return Err(LabourError::NotFound);
    };

    Ok(vec![LabourEvent::LabourPlanUpdated(LabourPlanUpdated {
        labour_id: cmd.labour_id,
        first_labour: cmd.first_labour,
        due_date: cmd.due_date,
        labour_name: cmd.labour_name,
    })])
}

pub fn handle_begin_labour(
    state: Option<&Labour>,
    cmd: BeginLabour,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let current_phase = labour.phase();

    if current_phase != &LabourPhase::PLANNED {
        return Err(LabourError::InvalidStateTransition(
            current_phase.to_string(),
            LabourPhase::EARLY.to_string(),
        ));
    }
    Ok(vec![LabourEvent::LabourBegun(LabourBegun {
        labour_id: cmd.labour_id,
        start_time: Utc::now(),
    })])
}

pub fn handle_complete_labour(
    state: Option<&Labour>,
    cmd: CompleteLabour,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let current_phase = labour.phase();

    if current_phase == &LabourPhase::COMPLETE {
        return Err(LabourError::InvalidStateTransition(
            current_phase.to_string(),
            LabourPhase::COMPLETE.to_string(),
        ));
    }

    if labour.find_active_contraction().is_some() {
        return Err(LabourError::ValidationError(
            "Cannot complete labour with active contraction".to_string(),
        ));
    }

    Ok(vec![LabourEvent::LabourCompleted(LabourCompleted {
        labour_id: cmd.labour_id,
        notes: cmd.notes,
        end_time: Utc::now(),
    })])
}

pub fn handle_send_labour_invite(
    state: Option<&Labour>,
    cmd: SendLabourInvite,
) -> Result<Vec<LabourEvent>, LabourError> {
    // TODO rate limiting checks per invite_email
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let current_phase = labour.phase();

    if current_phase == &LabourPhase::COMPLETE {
        return Err(LabourError::InvalidCommand(
            "Cannot invite to completed labour".to_string(),
        ));
    }

    Ok(vec![LabourEvent::LabourInviteSent(LabourInviteSent {
        labour_id: cmd.labour_id,
        invite_email: cmd.invite_email,
    })])
}

pub fn handle_delete_labour(
    state: Option<&Labour>,
    cmd: DeleteLabour,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let current_phase = labour.phase();

    if current_phase != &LabourPhase::COMPLETE {
        return Err(LabourError::InvalidCommand(
            "Cannot delete active labour".to_string(),
        ));
    }

    Ok(vec![LabourEvent::LabourDeleted(LabourDeleted {
        labour_id: cmd.labour_id,
    })])
}
