from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_v1_router
from contextlib import asynccontextmanager
from app.orm.base import Base
from app.orm.engine import engine
from app.orm.db_user import User
from app.orm.deadline import Deadline


# Create FastAPI app instance
app = FastAPI(
    title="AI Healthcare Assistant API",
    description="REST API for AI Healthcare Assistant focused on Dutch insurance matters for international students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    # lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_v1_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

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
