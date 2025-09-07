from __future__ import annotations
from typing import Dict, Any
from loguru import logger

def log_event(event: str, props: Dict[str, Any]) -> None:
    # Replace with Segment/Snowflake/BigQuery writers
    logger.info(f"analytics.{event}: {props}")
