from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.stt import router as stt_router

app = FastAPI(
    title="KIT VIBE CODING AI",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(stt_router)