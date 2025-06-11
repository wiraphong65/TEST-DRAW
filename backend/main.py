from fastapi import FastAPI
from .database import Base, engine
from . import models # Import all models to ensure they are registered with Base

from .routers import auth as auth_router, projects as projects_router, topology as topology_router # Import routers

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(auth_router.router)
app.include_router(projects_router.router)
app.include_router(topology_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
