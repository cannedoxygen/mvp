# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.routes import games, odds, simulations
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Baseball Betting Simulator API",
        description="API for the Baseball Betting Simulator, providing game data, odds, and simulation results",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(
        games.router,
        prefix=f"{settings.API_PREFIX}/games",
        tags=["games"],
    )
    app.include_router(
        odds.router,
        prefix=f"{settings.API_PREFIX}/odds",
        tags=["odds"],
    )
    app.include_router(
        simulations.router,
        prefix=f"{settings.API_PREFIX}/simulations",
        tags=["simulations"],
    )
    
    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        return {
            "message": "Welcome to the Baseball Betting Simulator API",
            "docs": "/docs",
            "version": settings.ENV,
        }
    
    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        return {
            "status": "healthy",
            "version": "0.1.0",
            "environment": settings.ENV
        }
    
    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENV != "production",
    )