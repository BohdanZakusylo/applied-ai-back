from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.dependencies import get_current_user
from app.models.deadline import Deadline, DeadlineList, DeadlineCreate, DeadlineUpdate
from app.services.deadline_service import DeadlineService

router = APIRouter(
    prefix="/deadlines",
    tags=["deadlines"],
)


@router.post("", response_model=Deadline, status_code=status.HTTP_201_CREATED)
async def create_deadline(
    deadline_data: DeadlineCreate,
    user_id: int = Depends(get_current_user)
):
    """Create a new deadline for the current user"""
    deadline = await DeadlineService.create_deadline(user_id, deadline_data)
    # Convert SQLAlchemy model to dictionary for Pydantic
    return {
        "id": deadline.id,
        "user_id": deadline.user_id,
        "title": deadline.title,
        "due_date": deadline.due_date,
        "created_at": deadline.created_at,
        "updated_at": deadline.updated_at
    }


@router.get("", response_model=DeadlineList)
async def get_user_deadlines(
    user_id: int = Depends(get_current_user)
):
    """Get all deadlines for the current user"""
    deadlines = await DeadlineService.get_user_deadlines(user_id)
    # Convert SQLAlchemy objects to Pydantic-compatible dictionaries
    deadline_dicts = [
        {
            "id": d.id,
            "user_id": d.user_id,
            "title": d.title,
            "due_date": d.due_date,
            "created_at": d.created_at,
            "updated_at": d.updated_at
        } for d in deadlines
    ]
    return DeadlineList(items=deadline_dicts, total=len(deadline_dicts))


@router.get("/{deadline_id}", response_model=Deadline)
async def get_deadline(
    deadline_id: int,
    user_id: int = Depends(get_current_user)
):
    """Get a specific deadline by ID"""
    deadline = await DeadlineService.get_deadline_by_id(deadline_id, user_id)
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    # Convert SQLAlchemy model to dictionary for Pydantic
    return {
        "id": deadline.id,
        "user_id": deadline.user_id,
        "title": deadline.title,
        "due_date": deadline.due_date,
        "created_at": deadline.created_at,
        "updated_at": deadline.updated_at
    }


@router.patch("/{deadline_id}", response_model=Deadline)
async def update_deadline(
    deadline_id: int,
    deadline_data: DeadlineUpdate,
    user_id: int = Depends(get_current_user)
):
    """Update a deadline"""
    updated_deadline = await DeadlineService.update_deadline(deadline_id, user_id, deadline_data)
    if not updated_deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    # Convert SQLAlchemy model to dictionary for Pydantic
    return {
        "id": updated_deadline.id,
        "user_id": updated_deadline.user_id,
        "title": updated_deadline.title,
        "due_date": updated_deadline.due_date,
        "created_at": updated_deadline.created_at,
        "updated_at": updated_deadline.updated_at
    }


@router.delete("/{deadline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deadline(
    deadline_id: int,
    user_id: int = Depends(get_current_user)
):
    """Delete a deadline"""
    success = await DeadlineService.delete_deadline(deadline_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
