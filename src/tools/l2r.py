from __future__ import annotations
from typing import List, Dict, Any
import numpy as np
from joblib import load
from loguru import logger

class HighlightRanker:
    def __init__(self, model_path: str | None = None):
        self.model = None
        if model_path:
            try:
                self.model = load(model_path)
                logger.info(f"Loaded L2R model: {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load model at {model_path}: {e}")

    def features_for_indices(self, sentiments: List[float], subs_density: List[float], motion: List[float], idxs: List[int]) -> np.ndarray:
        feats = []
        n = len(sentiments)
        for i in idxs:
            s = sentiments[i] if i < n else 0.0
            d = subs_density[i] if i < len(subs_density) else 0.0
            m = motion[i] if i < len(motion) else 0.0
            # features: level + local context
            window = sentiments[max(0,i-2):min(n,i+3)]
            mean_local = float(np.mean(window)) if window else 0.0
            feats.append([s, d, m, mean_local])
        return np.asarray(feats, dtype=float)

    def rank(self, sentiments: List[float], subs_density: List[float], motion: List[float], candidate_idxs: List[int], topk: int=6) -> List[int]:
        if self.model is None:
            # Fallback: sort by (0.6*sentiment + 0.3*subs + 0.1*motion)
            scores = []
            for i in candidate_idxs:
                s = sentiments[i] if i < len(sentiments) else 0.0
                d = subs_density[i] if i < len(subs_density) else 0.0
                m = motion[i] if i < len(motion) else 0.0
                scores.append((0.6*s + 0.3*d + 0.1*m, i))
            scores.sort(reverse=True)
            return [i for _, i in scores[:topk]]
        X = self.features_for_indices(sentiments, subs_density, motion, candidate_idxs)
        y = self.model.predict_proba(X)[:,1] if hasattr(self.model, "predict_proba") else self.model.predict(X)
        order = list(np.argsort(-y))
        ranked = [candidate_idxs[i] for i in order[:topk]]
        return ranked
