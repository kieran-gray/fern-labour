use serde::{Deserialize, Serialize};

#[derive(PartialEq, Debug, Deserialize, Serialize)]
pub struct PubSubEvent {
    pub subscription: String,
    pub message: PubSubEventBody,
}

#[derive(PartialEq, Debug, Deserialize, Serialize)]
pub struct PubSubEventBody {
    pub data: String, // base64 encoded
    pub message_id: String,
    pub publish_time: String,
}
