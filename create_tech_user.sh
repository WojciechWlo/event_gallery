-- create_tech_user.sql

DO $$
DECLARE
    pass TEXT;
BEGIN
    pass := substring(md5(random()::text), 1, 12);
    RAISE NOTICE 'Creating user sql_event_gallery with password: %', pass;

    EXECUTE format('CREATE USER sql_event_gallery WITH PASSWORD %L', pass);

    EXECUTE format('GRANT ALL PRIVILEGES ON DATABASE %I TO sql_event_gallery', current_database());

    EXECUTE format('GRANT USAGE ON SCHEMA public TO sql_event_gallery');

    EXECUTE format('GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO sql_event_gallery');

    EXECUTE format(
        'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO sql_event_gallery'
    );
END;
$$;
