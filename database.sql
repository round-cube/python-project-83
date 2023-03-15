CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at timestamp WITH TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc')
);

CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id integer REFERENCES urls (id),
    status_code integer NULL,
    h1 VARCHAR NULL,
    title VARCHAR NULL,
    description VARCHAR NULL,
    created_at timestamp WITH TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc')
);