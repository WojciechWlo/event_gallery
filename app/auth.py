from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import bcrypt
from models import User
from database import get_db

security = HTTPBasic()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)) -> str:
    users = db.query(User).all()
    if len(users)<1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No users in database",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    user = users[0]

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user.name
