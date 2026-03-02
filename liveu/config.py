from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DemoConfig:
    input_video: Path
    output_dir: Path
    output_stem: str
    target_duration_seconds: float
    still_time_seconds: float
    target_fps: int
    audio_bitrate: str = "128k"
