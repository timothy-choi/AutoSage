from moviepy import VideoFileClip
import os

def extract_audio(video_path: str, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if output_path is None:
        base = os.path.splitext(video_path)[0]
        output_path = f"{base}.mp3"

    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(output_path)
        clip.close()
        return output_path
    except Exception as e:
        raise RuntimeError(f"Audio extraction failed: {e}")