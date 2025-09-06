from fastapi import FastAPI
from app.api.endpoints import chemicals, inventory_logs
from app.database.database import engine
from app.models.models import Base

app = FastAPI(
    title="SDS Chemical Inventory & Reporting System",
    description="A FastAPI backend for managing chemical inventory with Safety Data Sheet (SDS) information",
    version="1.0.0"
)

# Include routers
app.include_router(chemicals.router, tags=["chemicals"])
app.include_router(inventory_logs.router, tags=["inventory-logs"])


@app.on_event("startup")
async def startup_event():
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SDS Chemical Inventory & Reporting System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}