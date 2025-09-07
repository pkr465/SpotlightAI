from __future__ import annotations
from langgraph.graph import StateGraph, END
from .state import PromoState

from .nodes import ingest, transcode, asr, scene_detect, sentiment, highlight_rank, script_gen, edit_assemble, render, qc, personalize, ab_test, publish, analytics

def build_graph():
    g = StateGraph(PromoState)

    g.add_node("ingest", ingest.run)
    g.add_node("transcode", transcode.run)
    g.add_node("asr", asr.run)
    g.add_node("scene_detect", scene_detect.run)
    g.add_node("sentiment", sentiment.run)
    g.add_node("highlight_rank", highlight_rank.run)
    g.add_node("script_gen", script_gen.run)
    g.add_node("edit_assemble", edit_assemble.run)
    g.add_node("render", render.run)
    g.add_node("qc", qc.run)
    g.add_node("personalize", personalize.run)
    g.add_node("ab_test", ab_test.run)
    g.add_node("publish", publish.run)
    g.add_node("analytics", analytics.run)

    g.set_entry_point("ingest")

    g.add_edge("ingest", "transcode")
    g.add_edge("transcode", "asr")
    g.add_edge("asr", "scene_detect")
    g.add_edge("scene_detect", "sentiment")
    g.add_edge("sentiment", "highlight_rank")
    g.add_edge("highlight_rank", "script_gen")
    g.add_edge("script_gen", "edit_assemble")
    g.add_edge("edit_assemble", "render")
    g.add_edge("render", "qc")
    g.add_edge("qc", "personalize")
    g.add_edge("personalize", "ab_test")
    g.add_edge("ab_test", "publish")
    g.add_edge("publish", "analytics")
    g.add_edge("analytics", END)

    return g.compile()
