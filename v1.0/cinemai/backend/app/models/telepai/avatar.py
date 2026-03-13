# backend/app/models/telepai/avatar.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Avatar(Base):
    __tablename__ = "avatar"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    actress_id = Column(Integer, ForeignKey("actress.id"), nullable=False)

    actress = relationship("Actress", back_populates="avatars")
    presences = relationship("Presence", back_populates="avatar", cascade="all, delete-orphan")
    profiles = relationship("Profile", back_populates="avatar", cascade="all, delete-orphan")
