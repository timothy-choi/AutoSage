from moviepy import VideoFileClip, concatenate_videoclips
import os

def merge_videos(
    video_paths: list[str],
    output_path: str = "merged_output.mp4",
    with_crossfade: bool = False,
    crossfade_duration: float = 1.0,
    resize_to: tuple[int, int] = None
) -> str:
    if not video_paths:
        raise ValueError("No input video paths provided.")

    try:
        clips = []
        for path in video_paths:
            clip = VideoFileClip(path)
            if resize_to:
                clip = clip.resize(newsize=resize_to)
            clips.append(clip)

        if with_crossfade:
            final_clip = concatenate_videoclips(clips, method="compose", padding=-crossfade_duration)
        else:
            final_clip = concatenate_videoclips(clips, method="compose")

        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        final_clip.close()
        return output_path
    except Exception as e:
        raise RuntimeError(f"Video merge failed: {e}")