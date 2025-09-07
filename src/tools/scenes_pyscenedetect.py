from __future__ import annotations
from loguru import logger

try:
    from scenedetect import open_video, SceneManager
    from scenedetect.detectors import ContentDetector
except Exception:
    open_video = None
    SceneManager = None
    ContentDetector = None

def detect_scenes(video_path: str, threshold: float = 27.0) -> list[tuple[float, float]]:
    """Return list of (start_s, end_s) scene ranges."""
    if open_video is None:
        logger.warning("PySceneDetect not installed; returning mock scenes.")
        return [(0,10),(10,25),(25,40),(40,60),(60,90),(90,120)]
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    scene_manager.detect_scenes(video, show_progress=False)
    scenes = scene_manager.get_scene_list()
    ranges = []
    for s, e in scenes:
        ranges.append((s.get_seconds(), e.get_seconds()))
    if not ranges:
        ranges = [(0.0, max(1.0, video.duration.get_seconds() if video.duration else 60.0))]
    return ranges
