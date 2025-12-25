use std::rc::Rc;

use fern_labour_event_sourcing_rs::EventStoreTrait;
use tracing::{info, warn};
use worker::State;

pub struct WebSocketEventBroadcaster {
    event_store: Rc<dyn EventStoreTrait>,
}

impl WebSocketEventBroadcaster {
    pub fn create(event_store: Rc<dyn EventStoreTrait>) -> Self {
        Self { event_store }
    }

    pub fn broadcast_new_events(&self, state: &State, since_sequence: i64) -> anyhow::Result<()> {
        // TODO: not all websocket clients need or should receive all domain events.
        // They should be filtered by permissions and even potentially have info redacted.

        let new_events = self.event_store.events_since(since_sequence, 100)?;

        if new_events.is_empty() {
            return Ok(());
        }

        let websockets = state.get_websockets();

        info!(
            "Broadcasting {} new events to {} connected clients",
            new_events.len(),
            websockets.len()
        );

        for ws in websockets {
            for event in &new_events {
                if let Err(e) = ws.send(&event.event_data) {
                    warn!(error = ?e, "Failed to send event to WebSocket client");
                }
            }
        }

        Ok(())
    }
}
