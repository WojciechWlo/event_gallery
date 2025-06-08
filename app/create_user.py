from sqlalchemy.orm import Session
from models import User
import bcrypt
from database import get_db
from config import GUEST_NAME, GUEST_PASSWORD

def create_guest_user():
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        existing_user = db.query(User).filter(User.name == GUEST_NAME).first()

        if not existing_user:
            hashed = bcrypt.hashpw(GUEST_PASSWORD.encode(), bcrypt.gensalt())
            user = User(name=GUEST_NAME, hashed_password=hashed.decode())
            db.add(user)
            db.commit()
            print("Dodano użytkownika.")
        else:
            print("Użytkownik już istnieje.")
    finally:
        db_gen.close()