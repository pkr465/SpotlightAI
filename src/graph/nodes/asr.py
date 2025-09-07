from __future__ import annotations
from ..state import PromoState

async def run(state: PromoState) -> PromoState:
    # Stub: call Whisper/ASR and attach subtitles transcript to metadata
    state.metadata["subtitles"] = "Mock transcript..."
    return state
