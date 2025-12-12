use chrono::{DateTime, Utc};
use fern_labour_labour_shared::value_objects::contraction::duration::Duration;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Contraction {
    id: Uuid,
    labour_id: Uuid,
    duration: Duration,
    intensity: Option<u8>,
}

impl Contraction {
    pub fn start(contraction_id: Uuid, labour_id: Uuid, start_time: DateTime<Utc>) -> Self {
        Self {
            id: contraction_id,
            labour_id,
            duration: Duration::create(start_time, start_time).expect("Failed to create duration"),
            intensity: None,
        }
    }

    pub fn end(&mut self, end_time: DateTime<Utc>, intensity: u8) {
        let duration =
            Duration::create(*self.start_time(), end_time).expect("Failed to create duration");
        self.duration = duration;
        self.intensity = Some(intensity);
    }

    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn is_active(&self) -> bool {
        self.duration.start_time() == self.duration.end_time()
    }

    pub fn start_time(&self) -> &DateTime<Utc> {
        self.duration.start_time()
    }

    pub fn end_time(&self) -> &DateTime<Utc> {
        self.duration.end_time()
    }
}
