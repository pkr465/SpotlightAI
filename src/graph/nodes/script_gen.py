from __future__ import annotations
from ..state import PromoState
from ...agents.llm import LLMClient
import json

async def run(state: PromoState) -> PromoState:
    llm = LLMClient()
    highlights_desc = [f"clip_{i}" for i in range(len(state.highlight_paths))]
    text = await llm.chat("script_gen", {
        "title": state.show_title or "Untitled",
        "logline": state.logline or "N/A",
        "audience": (state.audiences[0] if state.audiences else "genpop"),
        "highlights": highlights_desc,
        "brand": "YourBrand"
    })
    try:
        state.script_json = json.loads(text)
    except Exception:
        state.script_json = {"script": text, "taglines": [], "keywords": []}
    return state
