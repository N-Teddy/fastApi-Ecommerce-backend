from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.timing_middleware import TimingMiddleware
import logging
from src.database import init_database
from contextlib import asynccontextmanager

from src.core.config import settings
from src.api.v1.router import api_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database()
    print("🚀 Application started")
    yield
    # Shutdown
    print("🛑 Application shutting down")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for E-Commerce Application",
    version="1.0.0",
    lifespan=lifespan,
     openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(TimingMiddleware)

@app.get("/")
def home():
    return {"message": "Hello Teddy! FastAPI is running 🚀"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)