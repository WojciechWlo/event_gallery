from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
from database import Base
from datetime import datetime
from enum import Enum

class MediaTypeEnum(str, Enum):
    image = "image"
    video = "video"

Base = declarative_base()

hasRole = Table(
    "hasRole", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String)
    
    roles = relationship("Role", secondary=hasRole, back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    users = relationship("User", secondary=hasRole, back_populates="roles")

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    description = Column(String)
    datetime = Column(DateTime, default=datetime.utcnow)
    media = relationship("Media", back_populates="upload", cascade="all, delete-orphan")


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    mediatype = Column(String, nullable=False)
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    upload = relationship("Upload", back_populates="media")