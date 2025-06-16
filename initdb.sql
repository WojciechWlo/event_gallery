CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY,
    nickname TEXT,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    mediatype TEXT NOT NULL CHECK(mediatype IN ('image', 'video')),
    upload_id INTEGER,
    FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION create_tech_user(p_username TEXT) RETURNS VOID AS $$
DECLARE
    pass TEXT;
BEGIN
    pass := substring(md5(random()::text), 1, 12);

    EXECUTE format('CREATE USER %I WITH PASSWORD %L', p_username, pass);

    EXECUTE format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', current_database(), p_username);

    EXECUTE format('GRANT USAGE ON SCHEMA public TO %I', p_username);

    EXECUTE format('GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO %I', p_username);

    EXECUTE format(
        'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO %I',
        p_username
    );
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    PERFORM create_tech_user('sql_event_gallery');
END;
$$;