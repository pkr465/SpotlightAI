from __future__ import annotations
from ..state import PromoState
from ...agents.llm import LLMClient
import json

async def run(state: PromoState) -> PromoState:
    if not state.script_json:
        return state
    llm = LLMClient()
    for seg in (state.audiences or ["genpop"]):
        text = await llm.chat("personalize", {
            "segment": seg,
            "locale": "en-US",
            "brand": "YourBrand"
        })
        try:
            state.personalized_variants[seg] = json.loads(text)
        except Exception:
            state.personalized_variants[seg] = {"script": text, "taglines": []}
    return state
