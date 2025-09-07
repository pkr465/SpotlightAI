from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

    storage_backend: str = os.getenv("STORAGE_BACKEND", "local")  # s3|gcs|local
    s3_bucket: str | None = os.getenv("S3_BUCKET")
    aws_region: str | None = os.getenv("AWS_REGION")
    gcs_bucket: str | None = os.getenv("GCS_BUCKET")
    local_media_root: str = os.getenv("LOCAL_MEDIA_ROOT", "/tmp/ott-media")

    ffmpeg_bin: str = os.getenv("FFMPEG_BIN", "ffmpeg")
    ffprobe_bin: str = os.getenv("FFPROBE_BIN", "ffprobe")

    app_env: str = os.getenv("APP_ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_workers: int = int(os.getenv("MAX_WORKERS", "4"))
    default_timeout_s: int = int(os.getenv("DEFAULT_TIMEOUT_S", "120"))

    analytics_sink: str = os.getenv("ANALYTICS_SINK", "local")
    segment_write_key: str | None = os.getenv("SEGMENT_WRITE_KEY")

    brand_name: str = os.getenv("BRAND_NAME", "YourBrand")

settings = Settings()
