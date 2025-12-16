-- Migration number: 0002 	 2025-12-16T21:38:00.000Z
CREATE TABLE subscription_status (
    subscription_id TEXT PRIMARY KEY,
    labour_id TEXT NOT NULL,
    subscriber_id TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_subscription_status_subscriber_id ON subscription_status (subscriber_id);

CREATE INDEX idx_subscription_status_updated_at_subscription_id ON subscription_status (
    updated_at DESC,
    subscription_id DESC
);