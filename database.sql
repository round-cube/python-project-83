CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at timestamp WITH TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc')
);