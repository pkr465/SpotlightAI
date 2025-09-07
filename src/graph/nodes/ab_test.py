from __future__ import annotations
from ..state import PromoState
from ...agents.llm import LLMClient
import json

async def run(state: PromoState) -> PromoState:
    llm = LLMClient()
    text = await llm.chat("ab_hypotheses", { "metadata": state.metadata | {"audiences": state.audiences} })
    try:
        state.metadata["ab_tests"] = json.loads(text)
    except Exception:
        state.metadata["ab_tests"] = [text]
    return state
