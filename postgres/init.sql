CREATE TYPE status AS ENUM ('AVAILABLE', 'NOT AVAILABLE');

CREATE TABLE IF NOT EXISTS ServiceStatus (
    ip text NOT NULL PRIMARY KEY,
    status status
);
