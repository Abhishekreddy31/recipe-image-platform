"""Recipe API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ...database import get_db
from ...models import Recipe, RecipeStep, CookingAction
from ...schemas import RecipeCreate, RecipeResponse
from ...nlp import ActionExtractor, ActionMatcher
from ...nlp.action_matcher import load_taxonomy_for_matcher
from ...config import settings
import json

router = APIRouter()

# Initialize NLP components (lazy loading)
_extractor = None

def get_extractor():
    """Lazy load NLP extractor"""
    global _extractor
    if _extractor is None:
        # Load taxonomy
        taxonomy_actions = load_taxonomy_for_matcher(settings.TAXONOMY_PATH)
        matcher = ActionMatcher(taxonomy_actions)
        _extractor = ActionExtractor(matcher, settings.SPACY_MODEL)
    return _extractor


@router.post("/", response_model=RecipeResponse, status_code=201)
async def create_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db)):
    """
    Create a new recipe with automatic action extraction

    - Extracts cooking actions from each step using NLP
    - Returns enriched recipe with action details
    """
    extractor = get_extractor()

    # Create recipe
    recipe = Recipe(
        title=recipe_data.title,
        description=recipe_data.description,
        metadata=recipe_data.metadata or {}
    )
    db.add(recipe)
    db.flush()  # Get recipe ID

    # Create steps with action extraction
    for step_data in recipe_data.steps:
        # Extract actions from instruction text
        extracted = extractor.extract_actions(step_data.instruction_text)

        # Convert action IDs to UUIDs
        action_ids = [UUID(action["action_id"]) for action in extracted]

        # Store confidence scores
        confidence_data = {
            action["action_id"]: action["confidence"]
            for action in extracted
        }

        step = RecipeStep(
            recipe_id=recipe.id,
            step_number=step_data.step_number,
            instruction_text=step_data.instruction_text,
            extracted_actions=action_ids,
            nlp_confidence=confidence_data
        )
        db.add(step)

    db.commit()
    db.refresh(recipe)

    # Enrich response with action details
    return _enrich_recipe_response(recipe, db)


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: UUID, db: Session = Depends(get_db)):
    """Get recipe by ID with enriched action details"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return _enrich_recipe_response(recipe, db)


@router.get("/", response_model=List[RecipeResponse])
async def list_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all recipes with pagination"""
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return [_enrich_recipe_response(recipe, db) for recipe in recipes]


def _enrich_recipe_response(recipe: Recipe, db: Session) -> dict:
    """Enrich recipe response with cooking action details"""
    recipe_dict = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "created_at": recipe.created_at,
        "metadata": recipe.metadata,
        "steps": []
    }

    for step in recipe.steps:
        # Get action details
        action_details = []
        if step.extracted_actions:
            actions = db.query(CookingAction).filter(
                CookingAction.id.in_(step.extracted_actions)
            ).all()

            for action in actions:
                action_details.append({
                    "id": str(action.id),
                    "canonical_name": action.canonical_name,
                    "description": action.description,
                    "category": action.category,
                    "image_url": action.image_url,
                    "thumbnail_url": action.thumbnail_url,
                    "attribution": action.attribution,
                    "license": action.license,
                    "confidence": step.nlp_confidence.get(str(action.id), 1.0) if step.nlp_confidence else 1.0
                })

        recipe_dict["steps"].append({
            "id": step.id,
            "step_number": step.step_number,
            "instruction_text": step.instruction_text,
            "extracted_actions": action_details
        })

    return recipe_dict
