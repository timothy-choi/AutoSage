import cv2
import os
from typing import List


def combine_videos(video_paths: List[str], output_path: str) -> None:
    if not video_paths:
        raise ValueError("No video paths provided")

    first_cap = cv2.VideoCapture(video_paths[0])
    if not first_cap.isOpened():
        raise RuntimeError(f"Failed to open video: {video_paths[0]}")

    fps = first_cap.get(cv2.CAP_PROP_FPS)
    width = int(first_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(first_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    first_cap.release()

    for path in video_paths:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {path}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            resized = cv2.resize(frame, (width, height))
            out.write(resized)
        cap.release()

    out.release()