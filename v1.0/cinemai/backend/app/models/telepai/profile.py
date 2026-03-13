from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    avatar_id = Column(Integer, ForeignKey("avatar.id", ondelete="CASCADE"), nullable=False)
    audio_reference_path = Column(String, nullable=False)
    note = Column(Text)
    prompt_voice_clone_json = Column(Text, nullable=False)

    avatar = relationship("Avatar", back_populates="profiles")
    lines = relationship("Line", back_populates="profile", cascade="all, delete-orphan")