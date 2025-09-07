from __future__ import annotations
from ..state import PromoState

async def run(state: PromoState) -> PromoState:
    # Stub: scene boundaries, duration estimate
    # In reality, compute actual duration
    state.duration_s = 120.0
    state.metadata["scenes"] = [(0, 10),(10,25),(25,40),(40,60),(60,90),(90,120)]
    return state
