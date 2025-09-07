from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PromoState(BaseModel):
    asset_uri: str
    local_asset_path: Optional[str] = None

    duration_s: float | None = None
    sentiments: List[float] = Field(default_factory=list)
    highlight_indices: List[int] = Field(default_factory=list)
    highlight_segments: List[tuple[float,float]] = Field(default_factory=list)
    highlight_paths: List[str] = Field(default_factory=list)

    show_title: str | None = None
    logline: str | None = None

    script_json: Dict[str, Any] | None = None
    personalized_variants: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

    render_path: Optional[str] = None
    published_uri: Optional[str] = None

    campaign_id: Optional[str] = None
    audiences: List[str] = Field(default_factory=list)
    target_formats: List[str] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(default_factory=dict)
