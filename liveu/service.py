from __future__ import annotations

from pathlib import Path

from .config import DemoConfig
from .converter import ConversionResult, convert_video_to_live_photo


def create_live_photo(
    input_video: str | Path,
    output_dir: str | Path,
    output_stem: str | None = None,
    target_duration_seconds: float = 3.0,
    still_time_seconds: float | None = None,
    target_fps: int = 30,
    audio_bitrate: str = "128k",
) -> ConversionResult:
    input_path = Path(input_video)
    output_path = Path(output_dir)
    stem = output_stem or f"{input_path.stem}_live"
    still_time = (
        still_time_seconds
        if still_time_seconds is not None
        else max(0.0, target_duration_seconds / 2)
    )

    config = DemoConfig(
        input_video=input_path,
        output_dir=output_path,
        output_stem=stem,
        target_duration_seconds=target_duration_seconds,
        still_time_seconds=still_time,
        target_fps=target_fps,
        audio_bitrate=audio_bitrate,
    )
    return convert_video_to_live_photo(config)
