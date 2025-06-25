from app.orm.engine import SessionLocal
from app.orm.models.feedback import Feedback
from app.models.feedback import FeedbackCreate
from fastapi import HTTPException, status
import bleach

class FeedbackService:

    @staticmethod
    def sanitize_input(text: str) -> str:
        return bleach.clean(text, tags=[], attributes={}, strip=True)

    @staticmethod
    def submit_feedback(data: FeedbackCreate):
        db = SessionLocal()
        try:
            sanitized_message = FeedbackService.sanitize_input(data.message)

            feedback = Feedback(
                category=data.category,
                message=sanitized_message,
                email=data.email
            )

            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            return feedback

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to submit feedback."
            )
        finally:
            db.close()
