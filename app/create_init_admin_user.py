import os
import bcrypt
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
ADMIN_LOGIN = os.getenv("ADMIN_LOGIN", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

engine = create_engine(DATABASE_URL, future=True)

hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()

with engine.begin() as conn:
    # 1️⃣ Sprawdź, czy użytkownik istnieje
    user = conn.execute(
        text("SELECT id FROM users WHERE name = :name"),
        {"name": ADMIN_LOGIN}
    ).first()

    if user:
        user_id = user.id
        print(f"User '{ADMIN_LOGIN}' already exists.")
    else:
        conn.execute(
            text("INSERT INTO users (name, hashed_password) VALUES (:name, :pwd)"),
            {"name": ADMIN_LOGIN, "pwd": hashed_password}
        )
        user_id = conn.execute(
            text("SELECT id FROM users WHERE name = :name"),
            {"name": ADMIN_LOGIN}
        ).scalar_one()
        print(f"User '{ADMIN_LOGIN}' added to database.")

    # 2️⃣ Upewnij się, że rola 'admin' istnieje
    role = conn.execute(
        text("SELECT id FROM roles WHERE name = 'admin'")
    ).first()

    if role:
        role_id = role.id
        print("Role 'admin' already exists.")
    else:
        conn.execute(
            text("INSERT INTO roles (name) VALUES ('admin')")
        )
        role_id = conn.execute(
            text("SELECT id FROM roles WHERE name = 'admin'")
        ).scalar_one()
        print("Role 'admin' added to database.")

    # 3️⃣ Przypisz rolę 'admin' użytkownikowi, jeśli jeszcze nie ma
    has_role = conn.execute(
        text("SELECT id FROM hasRole WHERE user_id = :uid AND role_id = :rid"),
        {"uid": user_id, "rid": role_id}
    ).first()

    if has_role:
        print(f"User '{ADMIN_LOGIN}' already has role 'admin' — skipping.")
    else:
        conn.execute(
            text("INSERT INTO hasRole (user_id, role_id) VALUES (:uid, :rid)"),
            {"uid": user_id, "rid": role_id}
        )
        print(f"Role 'admin' assigned to user '{ADMIN_LOGIN}'.")