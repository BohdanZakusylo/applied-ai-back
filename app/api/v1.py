from fastapi import APIRouter
from app.routers import auth, users, chat, feedback, deadline

# Create API v1 router
api_v1_router = APIRouter(prefix="/api/v1")

# Include all routers with their individual prefixes
api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(chat.router)
api_v1_router.include_router(feedback.router)
api_v1_router.include_router(deadline.router)
