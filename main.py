from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import api_v1_router

# Create FastAPI app instance
app = FastAPI(
    title="AI Healthcare Assistant API",
    description="REST API for AI Healthcare Assistant focused on Dutch insurance matters for international students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_v1_router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "AI Healthcare Assistant API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0",
        "api_version": "v1",
        "endpoints": "/api/v1/"
    }
