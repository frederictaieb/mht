# backend/app/models/telepai/line.py
from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class Line(Base):
    __tablename__ = "line"
    __table_args__ = (
        UniqueConstraint("speech_id", "line_order", name="uq_line_speech_order"),
    )

    id = Column(Integer, primary_key=True, index=True)
    speech_id = Column(Integer, ForeignKey("speech.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profile.id", ondelete="CASCADE"), nullable=False)
    line_order = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    speech = relationship("Speech", back_populates="lines")
    profile = relationship("Profile")