from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base


class Chapter(Base):
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True, index=True)
    chapter_number = Column(Integer, nullable=False, unique=True)

    presences = relationship("Presence", back_populates="chapter", cascade="all, delete-orphan")