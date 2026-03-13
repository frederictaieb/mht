# backend/app/models/telepai/actress.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Actress(Base):
    __tablename__ = "actress"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    avatars = relationship("Avatar", back_populates="actress", cascade="all, delete-orphan")