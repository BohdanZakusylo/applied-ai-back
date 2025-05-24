from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, users, chat, files, health

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

# Include all routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(files.router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "AI Healthcare Assistant API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }
