from __future__ import annotations
from ..state import PromoState
from ...tools.analytics import log_event

async def run(state: PromoState) -> PromoState:
    log_event("promo.generated", {
        "campaign_id": state.campaign_id,
        "audiences": state.audiences,
        "keywords": (state.script_json or {}).get("keywords", [])
    })
    return state
