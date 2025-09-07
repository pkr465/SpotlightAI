from __future__ import annotations
from ..state import PromoState
from ...tools.saliency import salient_crop_bbox
import cv2, os, tempfile
from pathlib import Path

def export_ar_variant(src_path: str, aspect_ratio: float, out_name: str) -> str:
    cap = cv2.VideoCapture(src_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    ret, frame = cap.read()
    if not ret:
        return src_path
    x,y,w,h = salient_crop_bbox(frame, aspect_ratio=aspect_ratio)
    out_h = 1280
    out_w = int(out_h * aspect_ratio)
    out_path = str(Path(tempfile.gettempdir()) / out_name)
    writer = cv2.VideoWriter(out_path, fourcc, fps, (out_w, out_h))
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while True:
        ret, frame = cap.read()
        if not ret: break
        crop = frame[y:y+h, x:x+w]
        resized = cv2.resize(crop, (out_w, out_h))
        writer.write(resized)
    writer.release()
    cap.release()
    return out_path

async def run(state: PromoState) -> PromoState:
    if not state.render_path:
        return state
    # Export requested aspect ratios using saliency crops
    variants = {}
    for fmt in (state.target_formats or ["9:16","16:9"]):
        if fmt == "9:16":
            outp = export_ar_variant(state.render_path, aspect_ratio=9/16, out_name="promo_9x16.mp4")
        elif fmt == "1:1":
            outp = export_ar_variant(state.render_path, aspect_ratio=1.0, out_name="promo_1x1.mp4")
        else:
            outp = export_ar_variant(state.render_path, aspect_ratio=16/9, out_name="promo_16x9.mp4")
        variants[fmt] = outp
    state.metadata["ar_variants"] = variants
    # Keep main render as is; publishing node can upload all variants
    return state
