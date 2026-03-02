from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from loguru import logger

from .config import DemoConfig
from .tools import require_tool, run_command


@dataclass(frozen=True)
class ConversionResult:
    photo_path: Path
    video_path: Path


def _bounded_still_time(config: DemoConfig) -> float:
    return max(
        0.0,
        min(config.still_time_seconds, config.target_duration_seconds - 0.01),
    )


def convert_video_to_live_photo(config: DemoConfig) -> ConversionResult:
    if not config.input_video.exists():
        raise FileNotFoundError(f"Input video not found: {config.input_video}")

    logger.info(
        "Start converting live photo \ninput_video={} \noutput_dir={}",
        config.input_video,
        config.output_dir,
    )

    try:
        require_tool("ffmpeg")
        makelive_bin = require_tool(
            "makelive", fallback_path=Path(".venv/bin/makelive")
        )

        config.output_dir.mkdir(parents=True, exist_ok=True)

        mov_path = config.output_dir / f"{config.output_stem}.mov"
        jpg_path = config.output_dir / f"{config.output_stem}.jpg"
        still_time = _bounded_still_time(config)

        if mov_path.exists():
            mov_path.unlink()
        if jpg_path.exists():
            jpg_path.unlink()

        run_command(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(config.input_video),
                "-t",
                str(config.target_duration_seconds),
                "-r",
                str(config.target_fps),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                "-c:a",
                "aac",
                "-b:a",
                config.audio_bitrate,
                str(mov_path),
            ]
        )

        run_command(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(still_time),
                "-i",
                str(mov_path),
                "-frames:v",
                "1",
                "-update",
                "1",
                "-q:v",
                "2",
                str(jpg_path),
            ]
        )

        run_command([makelive_bin, "--manual", str(jpg_path), str(mov_path)])
    except Exception as exc:
        logger.error(
            "Live photo conversion failed | input_video={} | output_dir={} | error={}",
            config.input_video,
            config.output_dir,
            exc,
        )
        raise

    # logger.success(
    #     "Live photo conversion succeeded \nphoto_output={} \nvideo_output={}",
    #     jpg_path,
    #     mov_path,
    # )
    return ConversionResult(photo_path=jpg_path, video_path=mov_path)
