CREATE SEQUENCE IF NOT EXISTS users_id_seq;
ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq');

-- UPLOADS
CREATE SEQUENCE IF NOT EXISTS uploads_id_seq;
ALTER TABLE uploads ALTER COLUMN id SET DEFAULT nextval('uploads_id_seq');

-- MEDIA
CREATE SEQUENCE IF NOT EXISTS media_id_seq;
ALTER TABLE media ALTER COLUMN id SET DEFAULT nextval('media_id_seq');