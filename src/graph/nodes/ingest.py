from __future__ import annotations
from ...tools.storage import Storage
from ..state import PromoState

async def run(state: PromoState) -> PromoState:
    s = Storage()
    state.local_asset_path = s.get(state.asset_uri)
    state.metadata.update({"ingested": True})
    return state
