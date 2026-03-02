from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from loguru import logger


def run_command(cmd: list[str]) -> None:
    try:
        is_ffmpeg = Path(cmd[0]).name == "ffmpeg"
        if is_ffmpeg:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
        else:
            subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        if Path(cmd[0]).name == "ffmpeg" and exc.stderr:
            logger.error("ffmpeg failed: {}", exc.stderr.strip().splitlines()[-1])
        raise


def require_tool(tool_name: str, fallback_path: Path | None = None) -> str:
    tool = shutil.which(tool_name)
    if tool:
        return tool

    if fallback_path and fallback_path.exists():
        return str(fallback_path)

    raise FileNotFoundError(f"Could not find `{tool_name}` in PATH.")
