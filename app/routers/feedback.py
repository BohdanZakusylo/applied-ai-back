from fastapi import APIRouter, status
from app.orm.feedback import Feedback
from app.models.feedback import FeedbackCreate
from app.services.feedback_service import FeedbackService

router = APIRouter()

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: FeedbackCreate):
    FeedbackService.submit_feedback(feedback)
    return {"message": "Feedback submitted successfully."}
