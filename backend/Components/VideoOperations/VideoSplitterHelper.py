import cv2
import os
from typing import List

def split_video(input_path: str, output_dir: str, chunk_duration: float) -> List[str]:
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input video file not found")
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    chunk_frames = int(chunk_duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    chunk_paths = []
    chunk_index = 0
    frame_index = 0

    out = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % chunk_frames == 0:
            if out:
                out.release()
            chunk_filename = os.path.join(output_dir, f"chunk_{chunk_index}.mp4")
            out = cv2.VideoWriter(chunk_filename, fourcc, fps, (width, height))
            chunk_paths.append(chunk_filename)
            chunk_index += 1

    cap.release()
    if out:
        out.release()

    return chunk_paths