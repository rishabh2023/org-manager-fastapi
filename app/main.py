from fastapi import FastAPI
from app.routers import organizations, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Organization Manager API")

# allow frontend (React at port 3000) to talk to backend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # include OPTIONS
    allow_headers=["*"],
)


app.include_router(health.router, prefix="/api")
app.include_router(organizations.router, prefix="/api")
