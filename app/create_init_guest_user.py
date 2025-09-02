import os
import bcrypt
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
GUEST_LOGIN = os.getenv("GUEST_LOGIN", "guest")
GUEST_PASSWORD = os.getenv("GUEST_PASSWORD", "password")

engine = create_engine(DATABASE_URL, future=True)

hashed_password = bcrypt.hashpw(GUEST_PASSWORD.encode(), bcrypt.gensalt()).decode()

with engine.begin() as conn:

    result = conn.execute(
        text("SELECT id FROM users WHERE name = :name"),
        {"name": GUEST_LOGIN}
    ).first()

    if result:
        print(f"User '{GUEST_LOGIN}' already exists - skipping.")
    else:
        conn.execute(
            text("INSERT INTO users (name, hashed_password) VALUES (:name, :pwd)"),
            {"name": GUEST_LOGIN, "pwd": hashed_password}
        )
        print(f"User '{GUEST_LOGIN}' added to database.")