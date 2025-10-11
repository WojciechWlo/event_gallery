from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import bcrypt
from models import User
from database import get_db

security = HTTPBasic()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except:
        return False

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)) -> str:
    
    user = db.query(User).filter(User.name == credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user.name
