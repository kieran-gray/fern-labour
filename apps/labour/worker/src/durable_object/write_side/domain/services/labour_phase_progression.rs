use fern_labour_labour_shared::value_objects::LabourPhase;

use crate::durable_object::write_side::domain::Labour;

const RECENT_CONTRACTION_COUNT: usize = 3;
const TRANSITION_INTENSITY_THRESHOLD: f64 = 8.0;
const TRANSITION_DURATION_THRESHOLD_MINS: f64 = 1.5;
const ACTIVE_INTENSITY_THRESHOLD: f64 = 6.0;
const ACTIVE_DURATION_THRESHOLD_MINS: f64 = 1.0;

pub struct LabourPhaseProgression;

impl LabourPhaseProgression {
    pub fn evaluate(labour: &Labour) -> Option<LabourPhase> {
        let current_phase = labour.phase();

        if *current_phase == LabourPhase::COMPLETE {
            return None;
        }

        let new_phase = Self::calculate_phase_from_contractions(labour)?;

        if new_phase > *current_phase {
            Some(new_phase)
        } else {
            None
        }
    }

    fn calculate_phase_from_contractions(labour: &Labour) -> Option<LabourPhase> {
        let contractions = labour.contractions();

        let recent: Vec<_> = contractions
            .iter()
            .rev()
            .filter(|c| c.intensity().is_some())
            .take(RECENT_CONTRACTION_COUNT)
            .collect();

        if recent.len() < RECENT_CONTRACTION_COUNT {
            return None;
        }

        let count = recent.len() as f64;
        let avg_intensity: f64 = recent
            .iter()
            .map(|c| c.intensity().unwrap() as f64)
            .sum::<f64>()
            / count;
        let avg_duration: f64 = recent.iter().map(|c| c.duration_minutes()).sum::<f64>() / count;

        if avg_intensity >= TRANSITION_INTENSITY_THRESHOLD
            && avg_duration >= TRANSITION_DURATION_THRESHOLD_MINS
        {
            Some(LabourPhase::TRANSITION)
        } else if avg_intensity >= ACTIVE_INTENSITY_THRESHOLD
            && avg_duration >= ACTIVE_DURATION_THRESHOLD_MINS
        {
            Some(LabourPhase::ACTIVE)
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{TimeZone, Utc};
    use uuid::Uuid;

    use crate::durable_object::write_side::domain::{LabourEvent, events::*};
    use fern_labour_event_sourcing_rs::Aggregate;

    fn create_labour_with_contractions(contraction_specs: &[(f64, u8)]) -> Labour {
        let labour_id = Uuid::now_v7();
        let mut events = vec![
            LabourEvent::LabourPlanned(LabourPlanned {
                labour_id,
                mother_id: "mother_1".to_string(),
                mother_name: "Test Mother".to_string(),
                first_labour: true,
                due_date: Utc::now(),
                labour_name: None,
            }),
            LabourEvent::LabourPhaseChanged(LabourPhaseChanged {
                labour_id,
                labour_phase: LabourPhase::PLANNED,
            }),
            LabourEvent::LabourBegun(LabourBegun {
                labour_id,
                start_time: Utc::now(),
            }),
            LabourEvent::LabourPhaseChanged(LabourPhaseChanged {
                labour_id,
                labour_phase: LabourPhase::EARLY,
            }),
        ];

        let base_time = Utc.with_ymd_and_hms(2024, 1, 1, 12, 0, 0).unwrap();
        for (i, (duration_mins, intensity)) in contraction_specs.iter().enumerate() {
            let contraction_id = Uuid::now_v7();
            let start = base_time + chrono::Duration::minutes(i as i64 * 10);
            let end = start + chrono::Duration::seconds((duration_mins * 60.0) as i64);

            events.push(LabourEvent::ContractionStarted(ContractionStarted {
                labour_id,
                contraction_id,
                start_time: start,
            }));
            events.push(LabourEvent::ContractionEnded(ContractionEnded {
                labour_id,
                contraction_id,
                end_time: end,
                intensity: *intensity,
            }));
        }

        Labour::from_events(&events).unwrap()
    }

    #[test]
    fn no_contractions_returns_none() {
        let labour = create_labour_with_contractions(&[]);
        assert_eq!(LabourPhaseProgression::evaluate(&labour), None);
    }

    #[test]
    fn low_intensity_returns_none() {
        let labour = create_labour_with_contractions(&[(1.0, 5), (1.0, 5), (1.0, 5)]);
        assert_eq!(LabourPhaseProgression::evaluate(&labour), None);
    }

    #[test]
    fn short_duration_returns_none() {
        let labour = create_labour_with_contractions(&[(0.5, 8), (0.5, 8), (0.5, 8)]);
        assert_eq!(LabourPhaseProgression::evaluate(&labour), None);
    }

    #[test]
    fn active_threshold_met_returns_active() {
        let labour = create_labour_with_contractions(&[(1.0, 6), (1.2, 7), (1.1, 6)]);
        assert_eq!(
            LabourPhaseProgression::evaluate(&labour),
            Some(LabourPhase::ACTIVE)
        );
    }

    #[test]
    fn transition_threshold_met_returns_transition() {
        let labour = create_labour_with_contractions(&[(1.5, 8), (1.6, 9), (1.7, 8)]);
        assert_eq!(
            LabourPhaseProgression::evaluate(&labour),
            Some(LabourPhase::TRANSITION)
        );
    }

    #[test]
    fn uses_last_5_contractions() {
        let labour = create_labour_with_contractions(&[
            (0.5, 2),
            (0.5, 2),
            (0.5, 2),
            (1.0, 6),
            (1.0, 7),
            (1.0, 6),
            (1.0, 7),
            (1.0, 6),
        ]);
        assert_eq!(
            LabourPhaseProgression::evaluate(&labour),
            Some(LabourPhase::ACTIVE)
        );
    }
}
