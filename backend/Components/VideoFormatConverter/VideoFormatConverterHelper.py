import os
import subprocess
from typing import List

def convert_video_format(input_path: str, output_format: str, output_dir: str = "converted_videos") -> str:
    try:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.{output_format}")

        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            output_path
        ]

        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg error: {e.stderr.decode().strip()}")
    except Exception as e:
        raise Exception(f"Failed to convert video: {str(e)}")

def extract_audio(input_path: str, output_dir: str = "audio_tracks") -> str:
    try:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.mp3")

        command = [
            "ffmpeg",
            "-i", input_path,
            "-q:a", "0",
            "-map", "a",
            output_path
        ]

        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg error: {e.stderr.decode().strip()}")
    except Exception as e:
        raise Exception(f"Failed to extract audio: {str(e)}")

def batch_convert_format(video_paths: List[str], output_format: str, output_dir: str = "converted_videos") -> List[str]:
    results = []
    for path in video_paths:
        try:
            converted = convert_video_format(path, output_format, output_dir)
            results.append(converted)
        except Exception as e:
            results.append(f"Error converting {path}: {str(e)}")
    return results