import cv2
import os
import numpy as np

def summarize_video(video_path: str, output_path: str, frame_skip: int = 30) -> None:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Input video file not found")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % frame_skip == 0:
            out.write(frame)
        frame_id += 1

    cap.release()
    out.release()

def extract_key_frames(video_path: str, threshold: float = 30.0) -> list:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Input video not found")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, prev = cap.read()
    if not ret:
        return []

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    key_frames = [0.0]
    frame_index = 1

    while True:
        ret, curr = cap.read()
        if not ret:
            break
        curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, curr_gray)
        mean_diff = diff.mean()
        if mean_diff > threshold:
            timestamp = round(frame_index / fps, 2)
            key_frames.append(timestamp)
        prev_gray = curr_gray
        frame_index += 1

    cap.release()
    return key_frames