import os
import subprocess

def embed_subtitles(video_path: str, subtitle_path: str, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")
    if not os.path.exists(subtitle_path):
        raise FileNotFoundError("Subtitle file not found")

    if output_path is None:
        base, _ = os.path.splitext(video_path)
        output_path = f"{base}_subtitled.mp4"

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={subtitle_path}",
        "-c:a", "copy",
        output_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise RuntimeError(f"Subtitle embedding failed: {result.stderr.decode()}")

    return output_path