from fastapi import FastAPI
from app.routers import organizations, health

app = FastAPI(title="Organization Manager API")

app.include_router(health.router, prefix="/api")
app.include_router(organizations.router, prefix="/api")
