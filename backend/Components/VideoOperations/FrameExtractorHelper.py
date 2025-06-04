import cv2
import os

def extract_frames(video_path: str, output_dir: str, interval: int = 30) -> list:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    count = 0
    saved_paths = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            frame_name = f"frame_{count}.jpg"
            frame_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(frame_path, frame)
            saved_paths.append(frame_path)

        count += 1

    cap.release()
    return saved_paths