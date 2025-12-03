-- Add migration script here
CREATE TABLE contact_messages_new (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    message TEXT NOT NULL,
    data TEXT,
    received_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO contact_messages_new (id, category, email, name, message, data, received_at)
SELECT id, category, email, name, message, data, strftime('%Y-%m-%dT%H:%M:%SZ', created_at, 'unixepoch')
FROM contact_messages;

DROP TABLE contact_messages;

ALTER TABLE contact_messages_new RENAME TO contact_messages;

CREATE INDEX idx_contact_messages_category ON contact_messages(category);
CREATE INDEX idx_contact_messages_received_at ON contact_messages(received_at);