from sqlalchemy.orm import Session
from models import User
import bcrypt
from database import get_db


def create_guest_user():
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        existing_user = db.query(User).filter(User.name == "Gosc").first()

        if not existing_user:
            hashed = bcrypt.hashpw("WeseleKN2025".encode(), bcrypt.gensalt())
            user = User(name="Gosc", hashed_password=hashed.decode())
            db.add(user)
            db.commit()
            print("Dodano użytkownika.")
        else:
            print("Użytkownik już istnieje.")
    finally:
        db_gen.close()  # wywoła db.close() z generatora