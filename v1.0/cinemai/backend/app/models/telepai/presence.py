from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class Presence(Base):
    __tablename__ = "presence"
    __table_args__ = (
        UniqueConstraint("chapter_id", "avatar_id", name="uq_presence_chapter_avatar"),
    )

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"), nullable=False)
    avatar_id = Column(Integer, ForeignKey("avatar.id"), nullable=False)

    chapter = relationship("Chapter", back_populates="presences")
    avatar = relationship("Avatar", back_populates="presences")
    speeches = relationship("Speech", back_populates="presence", cascade="all, delete-orphan")