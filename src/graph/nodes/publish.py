from __future__ import annotations
from ..state import PromoState
from ...tools.storage import Storage

async def run(state: PromoState) -> PromoState:
    if not state.render_path:
        return state
    s = Storage()
    dest = f"s3://{state.campaign_id or 'campaign'}/promo_final.mp4"
    state.published_uri = s.put(state.render_path, dest)
    return state
