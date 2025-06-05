from moviepy import VideoFileClip
import os

def convert_video_to_gif(
    input_path: str,
    output_path: str,
    start_time: float = 0,
    end_time: float = None,
    resize_width: int = None,
    fps: int = 10
) -> str:
    clip = VideoFileClip(input_path).subclip(start_time, end_time)

    if resize_width:
        clip = clip.resize(width=resize_width)

    clip.write_gif(output_path, fps=fps)
    clip.close()

    return output_path