import os
import subprocess
from typing import List

def compress_video(input_path: str, output_dir: str = "compressed_videos", crf: int = 28, preset: str = "medium") -> str:
    try:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_compressed.mp4")

        command = [
            "ffmpeg",
            "-i", input_path,
            "-vcodec", "libx264",
            "-crf", str(crf),
            "-preset", preset,
            output_path
        ]

        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg error: {e.stderr.decode().strip()}")
    except Exception as e:
        raise Exception(f"Failed to compress video: {str(e)}")

def batch_compress_videos(video_paths: List[str], output_dir: str = "compressed_videos", crf: int = 28, preset: str = "medium") -> List[str]:
    results = []
    for path in video_paths:
        try:
            output = compress_video(path, output_dir, crf, preset)
            results.append(output)
        except Exception as e:
            results.append(f"Error compressing {path}: {str(e)}")
    return results

def estimate_compression(input_path: str) -> dict:
    try:
        size_bytes = os.path.getsize(input_path)
        size_mb = round(size_bytes / (1024 * 1024), 2)
        return {
            "filename": os.path.basename(input_path),
            "size_mb": size_mb,
            "recommendation": "Use CRF 28 or lower for balance between size and quality"
        }
    except Exception as e:
        raise Exception(f"Failed to estimate compression: {str(e)}")