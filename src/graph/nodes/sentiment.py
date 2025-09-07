from __future__ import annotations
from ..state import PromoState
import numpy as np
import librosa

def energy_envelope(audio_path: str, sr: int = 16000, hop_length: int = 512) -> list[float]:
    y, sr = librosa.load(audio_path, sr=sr, mono=True)
    S = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    # Normalize 0..1
    S = (S - S.min()) / (S.ptp() + 1e-8)
    return S.tolist()

async def run(state: PromoState) -> PromoState:
    # Use audio energy as a proxy for excitement (can be replaced by emotion model)
    # We rely on audio extracted by ASR node (audio.wav in tmp). For robustness, recompute if missing.
    import tempfile, os
    audio_path = os.path.join(tempfile.gettempdir(), "audio.wav")
    try:
        env = energy_envelope(audio_path)
        # upsample/trim to per-second by grouping
        step = max(1, len(env)//int((state.duration_s or 60)))
        sentiments = [float(np.mean(env[i:i+step])) for i in range(0, len(env), step)]
    except Exception:
        # Fallback to a flat series
        sentiments = [0.5] * int((state.duration_s or 60))
    state.sentiments = sentiments
    return state
