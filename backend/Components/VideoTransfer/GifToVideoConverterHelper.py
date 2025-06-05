from moviepy import VideoFileClip
import os

def convert_gif_to_video(
    gif_path: str,
    output_path: str = "converted_video.mp4",
    fps: int = 24
) -> str:
    if not os.path.exists(gif_path):
        raise FileNotFoundError("GIF file not found.")

    clip = VideoFileClip(gif_path)
    clip.write_videofile(output_path, codec='libx264', audio=False, fps=fps)
    clip.close()

    return output_path