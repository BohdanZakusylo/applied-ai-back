from fastapi import APIRouter, status, Depends
from app.orm.feedback import Feedback
from app.models.feedback import FeedbackCreate
from app.services.feedback_service import FeedbackService
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def create_feedback(feedback: FeedbackCreate, current_user: str = Depends(get_current_user)):
    if (current_user):
      FeedbackService.submit_feedback(feedback)
      return {"message": "Feedback submitted successfully."}
