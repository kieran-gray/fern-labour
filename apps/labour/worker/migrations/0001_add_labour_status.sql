-- Migration number: 0001 	 2025-12-13T21:50:21.953Z
CREATE TABLE labour_status (
    labour_id TEXT PRIMARY KEY,
    mother_id TEXT NOT NULL,
    mother_name TEXT NOT NULL,
    current_phase TEXT NOT NULL,
    labour_name TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_labour_status_mother_id ON labour_status(mother_id);
CREATE INDEX idx_labour_status_updated_at_labour_id ON labour_status(updated_at DESC, labour_id DESC);
