"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
import os

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Recipe platform with automatic cooking technique image display"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists(settings.STATIC_DIR):
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Import routers
from .api.v1 import recipes, actions, nlp

# Include routers
app.include_router(recipes.router, prefix=f"{settings.API_V1_PREFIX}/recipes", tags=["recipes"])
app.include_router(actions.router, prefix=f"{settings.API_V1_PREFIX}/actions", tags=["actions"])
app.include_router(nlp.router, prefix=f"{settings.API_V1_PREFIX}/nlp", tags=["nlp"])

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"{settings.APP_NAME} v{settings.VERSION} started!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "api": settings.API_V1_PREFIX
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
