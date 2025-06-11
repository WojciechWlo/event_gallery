CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hashed_password TEXT
);

CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    mediatype TEXT NOT NULL CHECK(mediatype IN ('image', 'video')),
    upload_id INTEGER,
    FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE CASCADE
);
