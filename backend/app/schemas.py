"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# Recipe Step Schemas
class RecipeStepCreate(BaseModel):
    step_number: int = Field(ge=1, description="Step number (1-indexed)")
    instruction_text: str = Field(min_length=5, max_length=2000)

class RecipeStepResponse(BaseModel):
    id: UUID
    step_number: int
    instruction_text: str
    extracted_actions: List[Dict[str, Any]]  # List of action details

    class Config:
        from_attributes = True

# Recipe Schemas
class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    steps: List[RecipeStepCreate] = Field(min_items=1)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class RecipeResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    steps: List[RecipeStepResponse]
    created_at: datetime
    metadata: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

# Cooking Action Schemas
class CookingActionResponse(BaseModel):
    id: UUID
    canonical_name: str
    description: Optional[str]
    category: str
    image_url: Optional[str]
    thumbnail_url: Optional[str]
    attribution: Optional[str]
    license: Optional[str]

    class Config:
        from_attributes = True

# NLP Testing Schema
class NLPExtractRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

class NLPExtractResponse(BaseModel):
    text: str
    extracted_actions: List[Dict[str, Any]]
