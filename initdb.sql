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