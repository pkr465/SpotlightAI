from __future__ import annotations
from ..state import PromoState
from ...tools.scenes_pyscenedetect import detect_scenes
from ...tools.video import probe

async def run(state: PromoState) -> PromoState:
    scenes = detect_scenes(state.local_asset_path or "", threshold=27.0)
    state.metadata["scenes"] = scenes
    # Estimate duration
    if scenes:
        state.duration_s = max(e for _, e in scenes)
    else:
        info = probe(state.local_asset_path or "")
        try:
            state.duration_s = float(info.get("format", {}).get("duration", 120.0))
        except Exception:
            state.duration_s = 120.0
    return state
