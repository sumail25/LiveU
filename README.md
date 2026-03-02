# LiveU - Video to Apple Live Photo

将用户上传的视频转换为可被 Apple Photos 识别的 Live Photo 资源（`JPG + MOV`）。

## 目标
- 输入：用户上传视频（如 `mp4` / `mov`）
- 输出：配对好的 Live Photo 资源（推荐先返回 `zip`，内含 `photo.jpg` 和 `video.mov`）
- 技术栈：Python（优先）+ macOS 工具链

## 环境要求
- macOS（建议 Apple Silicon/Intel 均可）
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Homebrew
- ffmpeg（用于视频转码与抽帧）

## 依赖安装
1. 安装系统依赖（ffmpeg）：
```bash
brew install ffmpeg
```

2. 初始化 Python 环境并安装项目依赖：
```bash
uv init --name liveu --python 3.11
uv add loguru makelive
```

3. 验证：
```bash
ffmpeg -version
uv run python -c "import loguru, makelive; print('deps ok')"
```

## VSCode 建议
- 使用仓库内解释器：`.venv/bin/python`
- 终端里运行命令优先用 `uv run <cmd>`

## 运行 Demo
```bash
uv run python demo.py
```

默认输入：
- `debug/videos/sample.mp4`

默认输出：
- `debug/output/live_photo_demo/sample_live.jpg`
- `debug/output/live_photo_demo/sample_live.mov`

## 代码结构
- `liveu/config.py`：输入输出和转换参数配置
- `liveu/converter.py`：核心转换流程（ffmpeg + makelive）
- `liveu/tools.py`：命令执行与工具发现
- `liveu/service.py`：对外调用函数 `create_live_photo(...)`
- `demo.py`：本地 demo，直接调用 `create_live_photo(...)`

## 外部调用示例
```python
from liveu import create_live_photo

result = create_live_photo(
    input_video="debug/videos/sample.mp4",
    output_dir="debug/output/live_photo_demo",
    output_stem="sample_live",
    target_duration_seconds=3.0,
    still_time_seconds=1.5,
    target_fps=30,
)

print(result.photo_path, result.video_path)
```

## Milestones
- Milestone 1 (2026-03-02): 本地 Live Photo 转换链路完成并验证通过
  - 已提供函数接口 `create_live_photo(...)` 供外部调用
  - 已完成模块化结构（`liveu/`）与 `demo.py` 调用示例
  - 输入测试视频 `debug/videos/sample.mp4` 可稳定输出可导入相册的 `JPG + MOV`
  - 日志已统一为 `loguru`，并精简为开始/结束关键日志

## 说明
- 本项目优先实现“可导入 Photos 的 Live Photo”。
- “可设为动态壁纸”有额外限制，不作为第一阶段目标。
