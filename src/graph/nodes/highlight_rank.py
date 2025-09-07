from __future__ import annotations
from ..state import PromoState
from ...tools import nlp, video
from pathlib import Path
import tempfile

async def run(state: PromoState) -> PromoState:
    idxs = nlp.rank_highlights(state.sentiments, topk=6, min_gap=5)
    segs = nlp.segments_from_indices(idxs, window_s=2.5, pad_s=0.5)
    state.highlight_indices = idxs
    state.highlight_segments = segs
    # Cut clips
    tmpd = tempfile.mkdtemp(prefix="clips_")
    paths = video.cut_segments(state.local_asset_path or "", segs, tmpd)
    state.highlight_paths = paths
    return state
