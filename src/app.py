from __future__ import annotations
from fastapi import FastAPI
from .api.routers import router as api_router

app = FastAPI(title="OTT Promo Agent")
app.include_router(api_router)

@app.get("/health")
def health():
    return {"ok": True}
