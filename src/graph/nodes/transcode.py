from __future__ import annotations
from ..state import PromoState

async def run(state: PromoState) -> PromoState:
    # Stub: in real life ensure codec & mezzanine format.
    state.metadata.update({"transcoded": True})
    return state
