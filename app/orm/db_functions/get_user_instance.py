from app.orm.engine import SessionLocal
from fastapi import HTTPException, status
from app.orm.models.db_user import User
from functools import wraps

def decorator_get_user_instance(func):
    @wraps(func)
    def wrapper(user_id: int, *args, **kwargs):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            return func(user, db, *args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error getting user."
            )
        finally:
            db.close()
    return wrapper