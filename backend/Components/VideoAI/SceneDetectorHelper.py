import cv2
import os

def detect_scenes(video_path: str, threshold: float = 30.0) -> list:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    scene_changes = []
    ret, prev_frame = cap.read()
    frame_id = 1

    if not ret:
        cap.release()
        return []

    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, curr_frame = cap.read()
        if not ret:
            break

        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(curr_frame_gray, prev_frame_gray)
        mean_diff = diff.mean()

        if mean_diff > threshold:
            scene_changes.append(frame_id)

        prev_frame_gray = curr_frame_gray
        frame_id += 1

    cap.release()
    return scene_changes