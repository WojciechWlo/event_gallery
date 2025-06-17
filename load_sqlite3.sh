#!/bin/bash

DB_FILE="/app/db.sqlite3"

if [ ! -f "$DB_FILE" ]; then
  echo "Creating SQLite DB from initdb.dev.sql..."
  sqlite3 "$DB_FILE" < /initdb.dev.sql
else
  echo "DB already exists, skipping init."
fi

exec "$@"