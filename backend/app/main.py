from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.all import router as all_router
from app.routers.health import router as health_router

app = FastAPI(title="Personal Site API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(all_router)
app.include_router(health_router)
