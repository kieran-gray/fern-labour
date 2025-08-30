CREATE TABLE notifications(
    id uuid NOT NULL,
    status varchar NOT NULL,
    notification_type varchar NOT NULL,
    destination varchar NOT NULL,
    template varchar NOT NULL,
    data jsonb NOT NULL,
    metadata jsonb,
    external_id varchar,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    PRIMARY KEY(id)
);