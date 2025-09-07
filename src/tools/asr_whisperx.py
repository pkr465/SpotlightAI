from __future__ import annotations
from loguru import logger

try:
    import whisperx  # type: ignore
except Exception:
    whisperx = None  # type: ignore

def transcribe_aligned(audio_path: str, device: str = "cpu") -> dict:
    """Return dict with keys: 'text', 'segments' [{start, end, text}]"""
    if whisperx is None:
        logger.warning("whisperx not installed; returning mock transcript.")
        return {"text": "Mock transcript...", "segments": [{"start":0.0,"end":3.0,"text":"Hello world"}]}
    model = whisperx.load_model("large-v3", device)
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=16)
    # alignment model (optional)
    try:
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device=device)
    except Exception as e:
        logger.warning(f"Alignment failed: {e}")
    # Normalize output
    segs = [{"start": s.get("start", 0.0), "end": s.get("end", 0.0), "text": s.get("text","")} for s in result.get("segments", [])]
    return {"text": " ".join(s['text'] for s in segs), "segments": segs}
