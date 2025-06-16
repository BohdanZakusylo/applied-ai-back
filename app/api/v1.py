from fastapi import APIRouter
from app.routers import auth, users, chat, feedback, deadline

# Create API v1 router
api_v1_router = APIRouter(prefix="/api/v1")

# Include all routers with their individual prefixes
api_v1_router.include_router(auth.router, tags=["Authentication"])
api_v1_router.include_router(users.router, tags=["Users"]) 
api_v1_router.include_router(chat.router, tags=["Chat"])
api_v1_router.include_router(feedback.router, tags=["Feedback"])
api_v1_router.include_router(deadline.router, tags=["Deadlines"])
