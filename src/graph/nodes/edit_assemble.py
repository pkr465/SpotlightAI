from __future__ import annotations
from ..state import PromoState
from ...tools import video
from pathlib import Path
import tempfile

async def run(state: PromoState) -> PromoState:
    # Simple concat of highlight clips; overlay/branding omitted in stub
    outp = str(Path(tempfile.gettempdir()) / "promo_concat.mp4")
    video.concat(state.highlight_paths, outp)
    state.render_path = outp
    return state
