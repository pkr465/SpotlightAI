from __future__ import annotations
from ..config import settings
from pathlib import Path
from loguru import logger
import shutil, os

class Storage:
    def __init__(self):
        self.backend = settings.storage_backend
        self.local_root = Path(settings.local_media_root)
        self.local_root.mkdir(parents=True, exist_ok=True)

    def get(self, uri: str) -> str:
        # For demo: if s3/gcs, pretend we download to local cache.
        target = self.local_root / (uri.replace('://','_').replace('/','_'))
        if not target.exists():
            logger.info(f"[mock] fetching {uri} -> {target}")
            target.write_bytes(b"mock-video-content")
        return str(target)

    def put(self, local_path: str, dest_uri: str) -> str:
        # For demo: copy to local area to simulate upload
        dest = self.local_root / (dest_uri.replace('://','_').replace('/','_'))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(local_path, dest)
        logger.info(f"[mock] stored {local_path} -> {dest_uri}")
        return dest_uri
