use anyhow::Result;
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
    pub fn start(contraction_id: Uuid, labour_id: Uuid, start_time: DateTime<Utc>) -> Result<Self> {
        let duration = Duration::create(start_time, start_time)?;
        Ok(Self {
            id: contraction_id,
            labour_id,
            duration,
            intensity: None,
        })
    }

    pub fn end(&mut self, end_time: DateTime<Utc>, intensity: u8) -> Result<()> {
        let duration = Duration::create(*self.start_time(), end_time)?;
        self.duration = duration;
        self.intensity = Some(intensity);
        Ok(())
    }

    pub fn update(
        &mut self,
        start_time: Option<DateTime<Utc>>,
        end_time: Option<DateTime<Utc>>,
        intensity: Option<u8>,
    ) -> Result<()> {
        let new_start = start_time.unwrap_or(*self.start_time());
        let new_end = end_time.unwrap_or(*self.end_time());

        let duration = Duration::create(new_start, new_end)?;
        self.duration = duration;

        if let Some(intensity_value) = intensity {
            self.intensity = Some(intensity_value);
        }

        Ok(())
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
