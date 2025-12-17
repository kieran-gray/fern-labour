use base64::{Engine, prelude::BASE64_URL_SAFE_NO_PAD};
use fern_labour_event_sourcing_rs::{Cursor, PaginatedResponse};

pub fn build_paginated_response<T: Cursor>(
    mut items: Vec<T>,
    limit: usize,
) -> PaginatedResponse<T> {
    let has_more = items.len() > limit;
    if has_more {
        items.pop();
    }

    let next_cursor = has_more.then(|| items.last()).flatten().map(|last_item| {
        let cursor_str = format!("{}|{}", last_item.updated_at().to_rfc3339(), last_item.id());
        BASE64_URL_SAFE_NO_PAD.encode(cursor_str)
    });

    PaginatedResponse {
        data: items,
        next_cursor,
        has_more,
    }
}
