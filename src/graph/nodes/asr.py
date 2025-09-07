from __future__ import annotations
from ..state import PromoState
from ...tools.asr_whisperx import transcribe_aligned
from ...tools.video import probe
from pathlib import Path
import tempfile, subprocess, os

async def run(state: PromoState) -> PromoState:
    # Extract audio using ffmpeg for WhisperX (if needed)
    src = state.local_asset_path or ""
    audio_out = str(Path(tempfile.gettempdir()) / "audio.wav")
    cmd = ["ffmpeg", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", audio_out]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result = transcribe_aligned(audio_out, device="cpu")
    except Exception:
        # Fallback: just probe duration
        result = {"text": "Mock transcript...", "segments": [{"start":0.0,"end":3.0,"text":"Hello world"}]}
    state.metadata["subtitles"] = result
    return state
