from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from fastapi import HTTPException, status

from app.orm.engine import SessionLocal
from app.orm.deadline import Deadline
from app.models.deadline import DeadlineCreate, DeadlineUpdate


class DeadlineService:

    @staticmethod
    async def create_deadline(user_id: int, deadline_data: DeadlineCreate) -> Deadline:
        """Create a new deadline for a user"""
        db = SessionLocal()
        try:
            new_deadline = Deadline(
                title=deadline_data.title,
                due_date=deadline_data.due_date,
                user_id=user_id,
                created_at=datetime.utcnow()
            )
            
            db.add(new_deadline)
            db.commit()
            db.refresh(new_deadline)
            
            return new_deadline
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create deadline: {str(e)}"
            )
        finally:
            db.close()

    @staticmethod
    async def get_user_deadlines(user_id: int) -> List[Deadline]:
        """Get all deadlines for a specific user"""
        db = SessionLocal()
        try:
            query = select(Deadline).where(Deadline.user_id == user_id)
            result = db.execute(query)
            
            return list(result.scalars().all())
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve deadlines: {str(e)}"
            )
        finally:
            db.close()

    @staticmethod
    async def get_deadline_by_id(deadline_id: int, user_id: int) -> Optional[Deadline]:
        """Get a specific deadline by ID (ensuring it belongs to the specified user)"""
        db = SessionLocal()
        try:
            query = select(Deadline).where(
                (Deadline.id == deadline_id) & 
                (Deadline.user_id == user_id)
            )
            result = db.execute(query)
            
            return result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve deadline: {str(e)}"
            )
        finally:
            db.close()

    @staticmethod
    async def update_deadline(
        deadline_id: int, 
        user_id: int, 
        deadline_data: DeadlineUpdate
    ) -> Optional[Deadline]:
        """Update an existing deadline"""
        db = SessionLocal()
        try:
            # First check if the deadline exists and belongs to the user
            deadline = await DeadlineService.get_deadline_by_id(deadline_id, user_id)
            
            if not deadline:
                return None
            
            # Need to get a fresh instance in this session
            deadline = db.query(Deadline).filter(
                (Deadline.id == deadline_id) & 
                (Deadline.user_id == user_id)
            ).first()
            
            if not deadline:
                return None
                
            # Update only the fields that were provided
            if deadline_data.title is not None:
                deadline.title = deadline_data.title
                
            if deadline_data.due_date is not None:
                deadline.due_date = deadline_data.due_date
                
            deadline.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(deadline)
            
            return deadline
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update deadline: {str(e)}"
            )
        finally:
            db.close()

    @staticmethod
    async def delete_deadline(deadline_id: int, user_id: int) -> bool:
        """Delete a deadline"""
        db = SessionLocal()
        try:
            # First check if the deadline exists and belongs to the user
            deadline = await DeadlineService.get_deadline_by_id(deadline_id, user_id)
            
            if not deadline:
                return False
            
            # Need to get a fresh instance in this session
            deadline = db.query(Deadline).filter(
                (Deadline.id == deadline_id) & 
                (Deadline.user_id == user_id)
            ).first()
            
            if not deadline:
                return False
                
            db.delete(deadline)
            db.commit()
            
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete deadline: {str(e)}"
            )
        finally:
            db.close()
