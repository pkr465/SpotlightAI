from __future__ import annotations
import cv2
import numpy as np
from loguru import logger

def salient_crop_bbox(frame: np.ndarray, aspect_ratio: float = 9/16) -> tuple[int,int,int,int]:
    """Compute a saliency-based crop bbox (x,y,w,h) for desired aspect.

    Falls back to center crop if saliency fails.
"""
    h, w = frame.shape[:2]
    target_h = h
    target_w = int(target_h * aspect_ratio)
    if target_w > w:
        target_w = w
        target_h = int(target_w / aspect_ratio)
    x0 = (w - target_w) // 2
    y0 = (h - target_h) // 2

    try:
        sal = cv2.saliency.StaticSaliencyFineGrained_create()
        success, salmap = sal.computeSaliency(frame)
        if success:
            salmap = (salmap * 255).astype("uint8")
            thr = cv2.threshold(salmap, 0, 255, cv2.THRESH_OTSU)[1]
            ys, xs = np.where(thr > 0)
            if len(xs) > 0:
                xmin, xmax = xs.min(), xs.max()
                ymin, ymax = ys.min(), ys.max()
                # Expand and enforce AR
                cx = (xmin + xmax) // 2
                cy = (ymin + ymax) // 2
                x0 = max(0, min(w - target_w, cx - target_w // 2))
                y0 = max(0, min(h - target_h, cy - target_h // 2))
    except Exception as e:
        logger.warning(f"Saliency failed; using center crop. {e}")
    return int(x0), int(y0), int(target_w), int(target_h)
