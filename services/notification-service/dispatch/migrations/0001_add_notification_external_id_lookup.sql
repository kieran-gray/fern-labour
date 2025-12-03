-- Migration number: 0001 	 2025-11-17T21:01:50.896Z
CREATE TABLE notification_external_id_lookup (
    external_id TEXT PRIMARY KEY,
    notification_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    provider TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_notification_id on notification_external_id_lookup(notification_id);
