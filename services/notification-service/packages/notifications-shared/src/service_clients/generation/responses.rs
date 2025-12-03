use serde::{Deserialize, Serialize};

use crate::value_objects::RenderedContent;

#[derive(Debug, Deserialize, Serialize)]
pub struct RenderResponse {
    pub rendered_content: RenderedContent,
}
