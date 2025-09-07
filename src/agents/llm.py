from __future__ import annotations
from typing import Optional, Dict, Any
from loguru import logger
from .prompts import PROMPTS
from ..config import settings

# We keep imports guarded so the project can run without all providers installed.
try:
    from langchain_openai import ChatOpenAI
except Exception:
    ChatOpenAI = None  # type: ignore

try:
    import anthropic
except Exception:
    anthropic = None  # type: ignore

class LLMClient:
    def __init__(self):
        self.provider = "openai" if settings.openai_api_key else "anthropic"
        logger.info(f"LLM provider set to: {self.provider}")

    async def chat(self, prompt_name: str, variables: Dict[str, Any]) -> str:
        tmpl = PROMPTS[prompt_name]
        prompt = tmpl.format(**variables)

        if self.provider == "openai" and ChatOpenAI:
            llm = ChatOpenAI(
                model=settings.openai_model,
                temperature=0.5,
                openai_api_key=settings.openai_api_key,
            )
            resp = await llm.ainvoke(prompt)  # type: ignore
            return resp.content  # type: ignore

        if self.provider == "anthropic" and anthropic:
            client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
            msg = await client.messages.create(
                model=settings.anthropic_model,
                max_tokens=1024,
                temperature=0.5,
                messages=[{ "role": "user", "content": prompt }],
            )
            # Simple text extraction
            try:
                return "".join([b.get("text","") for b in msg.content])
            except Exception:
                return str(msg)

        logger.warning("No LLM provider available; returning mock.")
        return f"[MOCK OUTPUT for {prompt_name}]\n" + prompt[:280]
