from __future__ import annotations
from ..state import PromoState
from ...tools import video
from ...tools.l2r import HighlightRanker
from pathlib import Path
import tempfile, numpy as np, cv2, os

def compute_motion_series(video_path: str, stride: int = 10) -> list[float]:
    cap = cv2.VideoCapture(video_path)
    prev = None
    scores = []
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        if i % stride == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev is not None:
                diff = cv2.absdiff(gray, prev)
                scores.append(float(np.mean(diff)/255.0))
            prev = gray
        i += 1
    cap.release()
    if not scores:
        scores = [0.0]
    # Stretch/aggregate to per-second estimates roughly
    return scores

def subtitles_density(subs: dict, duration_s: float, step_s: float=1.0) -> list[float]:
    segs = subs.get("segments", [])
    bins = int(max(1, duration_s/step_s))
    density = [0.0]*bins
    for s in segs:
        st = int(s.get("start",0.0)//step_s)
        en = int(s.get("end",0.0)//step_s)
        for t in range(st, min(bins, en+1)):
            density[t] += 1.0
    # Normalize
    m = max(density) if density else 1.0
    return [d/m if m>0 else 0.0 for d in density]

async def run(state: PromoState) -> PromoState:
    duration = state.duration_s or 60.0
    subs = state.metadata.get("subtitles", {"segments":[]})
    subs_dens = subtitles_density(subs, duration, step_s=1.0)

    motion = compute_motion_series(state.local_asset_path or "", stride=10)
    # Stretch motion to length of sentiments
    if len(motion) < len(state.sentiments):
        # simple repeat
        factor = int(np.ceil(len(state.sentiments)/max(1,len(motion))))
        motion = (motion * factor)[:len(state.sentiments)]
    else:
        motion = motion[:len(state.sentiments)]

    # Candidate indices: all seconds except first/last 2s
    cand = list(range(2, max(3, len(state.sentiments)-2)))

    ranker = HighlightRanker(model_path=os.environ.get("HIGHLIGHT_L2R_MODEL"))
    top = ranker.rank(state.sentiments, subs_dens, motion, cand, topk=6)

    # Create short segments around each index
    segs = [(max(0, i-0.5), i+2.5) for i in top]  # 3s snippets
    # Cut clips
    tmpd = tempfile.mkdtemp(prefix="clips_")
    paths = video.cut_segments(state.local_asset_path or "", segs, tmpd)

    state.highlight_indices = top
    state.highlight_segments = segs
    state.highlight_paths = paths
    # Keep some debug features
    state.metadata["features"] = {"sentiments": state.sentiments, "subs_density": subs_dens, "motion": motion}
    return state
