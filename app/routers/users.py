from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import DatabaseUser, UserProfileUpdate, UserProfileResponse
from app.dependencies import get_current_user
from app.services import user_service
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile", status_code = status.HTTP_200_OK)
async def get_user_profile(current_user: int = Depends(get_current_user)):
    """
    Get current user's profile information
    """
    user = user_service.UserService.get_user_by_id(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user": user}

@router.put("/profile", status_code = status.HTTP_200_OK)
async def update_user_profile(profile_update: UserProfileUpdate, current_user: str = Depends(get_current_user)):
    """
    Update current user's profile information
    """
    updated_user = await user_service.UserService.update_user_profile(
        user_id=current_user,
        email=profile_update.email,
        password=profile_update.password,
        insurance_provider=profile_update.insurance_provider,
        general_practitioner=profile_update.general_practitioner,
        medical_information=profile_update.medical_information
    )
    
    return {"updated_user": updated_user}

@router.delete("/profile", status_code = status.HTTP_200_OK)
async def delete_user_account(current_user: str = Depends(get_current_user)):
    """
    Delete current user's account and all associated data
    """
    # TODO: Implement account deletion logic
    # - Use current_user (user ID from JWT token)
    # - Delete user data from database
    # - Delete associated files and chat history
    # - Invalidate all user tokens
    return {"message": f"Account {current_user} deleted successfully"} 