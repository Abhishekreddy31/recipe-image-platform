"""Cooking Actions API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ...database import get_db
from ...models import CookingAction
from ...schemas import CookingActionResponse

router = APIRouter()


@router.get("/", response_model=List[CookingActionResponse])
async def list_actions(
    category: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all cooking actions, optionally filtered by category"""
    query = db.query(CookingAction)

    if category:
        query = query.filter(CookingAction.category == category)

    actions = query.offset(skip).limit(limit).all()
    return actions


@router.get("/{action_id}", response_model=CookingActionResponse)
async def get_action(action_id: UUID, db: Session = Depends(get_db)):
    """Get cooking action by ID"""
    action = db.query(CookingAction).filter(CookingAction.id == action_id).first()

    if not action:
        raise HTTPException(status_code=404, detail="Cooking action not found")

    return action
