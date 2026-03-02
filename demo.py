from __future__ import annotations

from pathlib import Path

from loguru import logger

from liveu import create_live_photo


def main() -> None:
    input_video = Path("debug/videos/sample.mp4")
    output_dir = Path("debug/output/live_photo_demo")

    result = create_live_photo(
        input_video=input_video,
        output_dir=output_dir,
        output_stem="sample_live",
        target_duration_seconds=3.0,
        still_time_seconds=1.5,
        target_fps=30,
        audio_bitrate="128k",
    )

    logger.success(
        "Demo finished \nphoto_output={} \nvideo_output={}",
        result.photo_path,
        result.video_path,
    )


if __name__ == "__main__":
    main()
