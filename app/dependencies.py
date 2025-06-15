from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.services.jwt_service import decode_jwt
from app.orm.engine import SessionLocal
from app.orm.db_user import User

# Define the security scheme for Swagger UI
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_jwt(credentials.credentials)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex)
        )
    
    if payload:
        user_id = payload["user_id"]

        session = SessionLocal()
        try:
            existing_and_valid_token = session.query(User).filter(
                User.id == user_id,
                User.token == credentials.credentials
            ).first()

            if not existing_and_valid_token:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="There is no such user"
                )

        except HTTPException:
            session.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occured, please try again"
            )
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error"
            )
        finally:
            session.close()

        return user_id