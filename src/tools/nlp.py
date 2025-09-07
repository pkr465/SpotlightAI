from __future__ import annotations
from typing import List, Dict, Any
import random

def mock_sentiment_timecourse(duration_s: float, step_s: float = 1.0) -> list[float]:
    # Replace with real emotion/sentiment model inference over time.
    n = int(duration_s / step_s)
    return [random.uniform(-1, 1) for _ in range(max(n, 1))]

def rank_highlights(sentiments: list[float], topk: int = 5, min_gap: int = 3) -> list[int]:
    # Naive peak picking
    idxs = sorted(range(len(sentiments)), key=lambda i: sentiments[i], reverse=True)
    picks = []
    for i in idxs:
        if all(abs(i - p) >= min_gap for p in picks):
            picks.append(i)
        if len(picks) >= topk:
            break
    return sorted(picks)

def segments_from_indices(indices: list[int], window_s: float = 3.0, pad_s: float = 0.5) -> list[tuple[float,float]]:
    return [(max(0, i*1.0 - pad_s), (i*1.0 + window_s + pad_s)) for i in indices]
