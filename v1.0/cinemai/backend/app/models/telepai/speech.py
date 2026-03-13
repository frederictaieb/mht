from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Speech(Base):
    __tablename__ = "speech"

    id = Column(Integer, primary_key=True, index=True)
    presence_id = Column(Integer, ForeignKey("presence.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=True)

    presence = relationship("Presence", back_populates="speeches")
    lines = relationship("Line", back_populates="speech", cascade="all, delete-orphan")