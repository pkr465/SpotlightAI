from __future__ import annotations
import subprocess, json, tempfile
from pathlib import Path
from ..config import settings
from loguru import logger

def probe(path: str) -> dict:
    cmd = [settings.ffprobe_bin, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path]
    try:
        out = subprocess.check_output(cmd)
        return json.loads(out.decode())
    except Exception as e:
        logger.warning(f"ffprobe failed: {e}")
        return {}

def cut_segments(path: str, segments: list[tuple[float,float]], out_dir: str) -> list[str]:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    outs = []
    for i, (start, end) in enumerate(segments):
        outp = str(Path(out_dir) / f"clip_{i:03d}.mp4")
        dur = max(0.1, end - start)
        cmd = [settings.ffmpeg_bin, "-y", "-ss", str(start), "-i", path, "-t", str(dur), "-c", "copy", outp]
        try:
            subprocess.check_call(cmd)
        except Exception as e:
            logger.warning(f"ffmpeg (copy) failed; retrying with re-encode: {e}")
            cmd = [settings.ffmpeg_bin, "-y", "-ss", str(start), "-i", path, "-t", str(dur), "-vf", "scale=1280:-1", "-c:v", "libx264", "-c:a", "aac", outp]
            subprocess.check_call(cmd)
        outs.append(outp)
    return outs

def concat(paths: list[str], out_path: str) -> str:
    list_file = Path(out_path).with_suffix(".txt")
    list_file.write_text("\n".join([f"file '{p}'" for p in paths]))
    cmd = [settings.ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", out_path]
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        logger.warning(f"concat (copy) failed; re-encoding: {e}")
        cmd = [settings.ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c:v", "libx264", "-c:a", "aac", out_path]
        subprocess.check_call(cmd)
    return out_path
