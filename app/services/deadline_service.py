from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm.deadline import Deadline
from app.models.deadline import DeadlineCreate, DeadlineUpdate


class DeadlineService:

    @staticmethod
    async def create_deadline(db: Session, user_id: int, deadline_data: DeadlineCreate) -> Deadline:
        """Create a new deadline for a user"""
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

    @staticmethod
    async def get_user_deadlines(db: Session, user_id: int) -> List[Deadline]:
        """Get all deadlines for a specific user"""
        query = select(Deadline).where(Deadline.user_id == user_id)
        result = db.execute(query)
        
        return list(result.scalars().all())

    @staticmethod
    async def get_deadline_by_id(db: Session, deadline_id: int, user_id: int) -> Optional[Deadline]:
        """Get a specific deadline by ID (ensuring it belongs to the specified user)"""
        query = select(Deadline).where(
            (Deadline.id == deadline_id) & 
            (Deadline.user_id == user_id)
        )
        result = db.execute(query)
        
        return result.scalar_one_or_none()

    @staticmethod
    async def update_deadline(
        db: Session, 
        deadline_id: int, 
        user_id: int, 
        deadline_data: DeadlineUpdate
    ) -> Optional[Deadline]:
        """Update an existing deadline"""
        deadline = await DeadlineService.get_deadline_by_id(db, deadline_id, user_id)
        
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

    @staticmethod
    async def delete_deadline(db: Session, deadline_id: int, user_id: int) -> bool:
        """Delete a deadline"""
        deadline = await DeadlineService.get_deadline_by_id(db, deadline_id, user_id)
        
        if not deadline:
            return False
            
        db.delete(deadline)
        db.commit()
        
        return True
