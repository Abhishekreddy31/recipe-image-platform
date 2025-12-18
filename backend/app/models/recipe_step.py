from sqlalchemy import Column, Integer, Text, JSON, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin

class RecipeStep(Base, UUIDMixin, TimestampMixin):
    """Recipe step model with extracted cooking actions"""
    __tablename__ = "recipe_steps"

    recipe_id = Column(String(36), ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    step_number = Column(Integer, nullable=False)
    instruction_text = Column(Text, nullable=False)

    # JSON array of extracted action IDs (SQLite compatible)
    extracted_actions = Column(JSON, default=list)

    # Store NLP confidence scores for each action
    nlp_confidence = Column(JSON)  # {action_id: confidence_score}

    # Relationships
    recipe = relationship("Recipe", back_populates="steps")

    def __repr__(self):
        return f"<RecipeStep(id={self.id}, recipe_id={self.recipe_id}, step={self.step_number})>"
