from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from ..graph.state import PromoState
from ..graph.builder import build_graph

router = APIRouter()

class RunRequest(BaseModel):
    asset_uri: str
    campaign_id: str | None = None
    audiences: list[str] = []
    target_formats: list[str] = []
    show_title: str | None = None
    logline: str | None = None

@router.post("/run")
async def run(req: RunRequest):
    graph = build_graph()
    state = PromoState(
        asset_uri=req.asset_uri,
        campaign_id=req.campaign_id,
        audiences=req.audiences,
        target_formats=req.target_formats,
        show_title=req.show_title,
        logline=req.logline,
    )
    out = await graph.ainvoke(state)
    return out.model_dump()
