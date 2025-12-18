from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from .base import Base, UUIDMixin, TimestampMixin

class CookingAction(Base, UUIDMixin, TimestampMixin):
    """Cooking action taxonomy with image metadata"""
    __tablename__ = "cooking_actions"

    canonical_name = Column(String(100), unique=True, nullable=False, index=True)
    synonyms = Column(ARRAY(Text), default=list)  # Array of synonym strings
    description = Column(Text)
    category = Column(String(50), index=True)  # cutting-prep, mixing-combining, etc.

    # Priority and difficulty
    priority = Column(Integer, default=1)  # 1=high, 3=low
    difficulty = Column(String(20))  # easy, medium, hard

    # Image metadata
    wikimedia_file_id = Column(String(255))  # e.g., "File:Dicing_onions.jpg"
    image_url = Column(Text)  # Full URL to processed image
    thumbnail_url = Column(Text)  # Thumbnail URL

    # Attribution (required for CC licenses)
    attribution = Column(Text)  # Full attribution text
    license = Column(String(50))  # e.g., "CC-BY-SA-4.0"

    def __repr__(self):
        return f"<CookingAction(id={self.id}, name={self.canonical_name})>"
