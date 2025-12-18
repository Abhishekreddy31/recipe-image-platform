from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin

class Recipe(Base, UUIDMixin, TimestampMixin):
    """Recipe model"""
    __tablename__ = "recipes"

    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    author_id = Column(String(100))  # Future: link to user table
    recipe_metadata = Column(JSON)  # Store servings, prep_time, cook_time, etc.

    # Relationships
    steps = relationship(
        "RecipeStep",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeStep.step_number"
    )

    def __repr__(self):
        return f"<Recipe(id={self.id}, title={self.title})>"
