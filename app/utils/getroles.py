from database import get_db
from models import User

def get_roles(username: str) -> list[str]:
    db_gen = get_db()
    db = next(db_gen)

    try:
        user = db.query(User).filter(User.name == username).first()
        if not user or not user.roles:
            return []

        return [role.name for role in user.roles]

    finally:
        db.close()