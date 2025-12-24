use chrono::Utc;
use fern_labour_labour_shared::value_objects::LabourUpdateType;
use uuid::Uuid;

use crate::durable_object::write_side::domain::{
    Labour, LabourError, LabourEvent,
    commands::labour_update::{
        DeleteLabourUpdate, PostApplicationLabourUpdate, PostLabourUpdate,
        UpdateLabourUpdateMessage, UpdateLabourUpdateType,
    },
    events::{
        LabourUpdateDeleted, LabourUpdateMessageUpdated, LabourUpdatePosted,
        LabourUpdateTypeUpdated,
    },
};

pub fn handle_post_labour_update(
    state: Option<&Labour>,
    cmd: PostLabourUpdate,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    if cmd.labour_update_type == LabourUpdateType::ANNOUNCEMENT && !labour.can_send_announcement() {
        return Err(LabourError::InvalidCommand(
            "Too soon since last announcement".to_string(),
        ));
    }

    Ok(vec![LabourEvent::LabourUpdatePosted(LabourUpdatePosted {
        labour_id: cmd.labour_id,
        labour_update_id: Uuid::now_v7(),
        labour_update_type: cmd.labour_update_type,
        message: cmd.message,
        application_generated: false,
        sent_time: Utc::now(),
    })])
}

pub fn handle_post_application_labour_update(
    state: Option<&Labour>,
    cmd: PostApplicationLabourUpdate,
) -> Result<Vec<LabourEvent>, LabourError> {
    if state.is_none() {
        return Err(LabourError::NotFound);
    };

    Ok(vec![LabourEvent::LabourUpdatePosted(LabourUpdatePosted {
        labour_id: cmd.labour_id,
        labour_update_id: Uuid::now_v7(),
        labour_update_type: LabourUpdateType::PRIVATE_NOTE,
        message: cmd.message,
        application_generated: true,
        sent_time: Utc::now(),
    })])
}

pub fn handle_update_labour_update_type(
    state: Option<&Labour>,
    cmd: UpdateLabourUpdateType,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let Some(labour_update) = labour.find_labour_update(cmd.labour_update_id) else {
        return Err(LabourError::InvalidCommand(
            "Labour update not found".to_string(),
        ));
    };

    if labour_update.labour_update_type() == &LabourUpdateType::ANNOUNCEMENT {
        return Err(LabourError::InvalidCommand(
            "Cannot update an announcement".to_string(),
        ));
    }

    if cmd.labour_update_type == LabourUpdateType::ANNOUNCEMENT && !labour.can_send_announcement() {
        return Err(LabourError::InvalidCommand(
            "Too soon since last announcement".to_string(),
        ));
    }

    Ok(vec![LabourEvent::LabourUpdateTypeUpdated(
        LabourUpdateTypeUpdated {
            labour_id: cmd.labour_id,
            labour_update_id: cmd.labour_update_id,
            labour_update_type: cmd.labour_update_type,
        },
    )])
}

pub fn handle_update_labour_update_message(
    state: Option<&Labour>,
    cmd: UpdateLabourUpdateMessage,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let Some(labour_update) = labour.find_labour_update(cmd.labour_update_id) else {
        return Err(LabourError::InvalidCommand(
            "Labour update not found".to_string(),
        ));
    };

    if labour_update.labour_update_type() == &LabourUpdateType::ANNOUNCEMENT {
        return Err(LabourError::InvalidCommand(
            "Cannot update an announcement".to_string(),
        ));
    }

    Ok(vec![LabourEvent::LabourUpdateMessageUpdated(
        LabourUpdateMessageUpdated {
            labour_id: cmd.labour_id,
            labour_update_id: cmd.labour_update_id,
            message: cmd.message,
        },
    )])
}

pub fn handle_delete_labour_update(
    state: Option<&Labour>,
    cmd: DeleteLabourUpdate,
) -> Result<Vec<LabourEvent>, LabourError> {
    let Some(labour) = state else {
        return Err(LabourError::NotFound);
    };

    let Some(_) = labour.find_labour_update(cmd.labour_update_id) else {
        return Err(LabourError::InvalidCommand(
            "Labour update not found".to_string(),
        ));
    };

    Ok(vec![LabourEvent::LabourUpdateDeleted(
        LabourUpdateDeleted {
            labour_id: cmd.labour_id,
            labour_update_id: cmd.labour_update_id,
        },
    )])
}
