from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.dependencies import get_current_user
from app.models.deadline import DeadlineCreate, DeadlineResponse, DeadlineUpdate, DeadlineListResponse
from app.services.deadline_service import DeadlineService

router = APIRouter(
    prefix="/deadlines",
    tags=["deadlines"],
)


@router.post("", response_model=DeadlineResponse, status_code=status.HTTP_201_CREATED)
async def create_deadline(
    deadline_data: DeadlineCreate,
    user_id: int = Depends(get_current_user)
):
    """Create a new deadline for the current user"""
    deadline = await DeadlineService.create_deadline(user_id, deadline_data)
    return deadline


@router.get("", response_model=DeadlineListResponse)
async def get_user_deadlines(
    user_id: int = Depends(get_current_user)
):
    """Get all deadlines for the current user"""
    deadlines = await DeadlineService.get_user_deadlines(user_id)
    return DeadlineListResponse(items=deadlines, total=len(deadlines))


@router.get("/{deadline_id}", response_model=DeadlineResponse)
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
    return deadline


@router.patch("/{deadline_id}", response_model=DeadlineResponse)
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
    return updated_deadline


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
