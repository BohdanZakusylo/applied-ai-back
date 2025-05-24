from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """
    API health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "service": "AI Healthcare Assistant API",
        "version": "1.0.0"
    } 