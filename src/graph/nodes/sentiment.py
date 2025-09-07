from __future__ import annotations
from ..state import PromoState
from ...tools import nlp

async def run(state: PromoState) -> PromoState:
    sentiments = nlp.mock_sentiment_timecourse(duration_s=state.duration_s or 60.0, step_s=1.0)
    state.sentiments = sentiments
    return state
