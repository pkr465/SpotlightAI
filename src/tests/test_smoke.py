import asyncio
from src.graph.builder import build_graph
from src.graph.state import PromoState

async def _run():
    g = build_graph()
    state = PromoState(asset_uri="s3://bucket/sample.mp4", audiences=["genpop"], campaign_id="cmp_smoke")
    out = await g.ainvoke(state)
    assert out.published_uri is not None

def test_graph_runs():
    asyncio.run(_run())
