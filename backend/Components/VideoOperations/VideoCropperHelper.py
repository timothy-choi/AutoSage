import cv2
import os

def crop_video(input_path: str, output_path: str, x: int, y: int, width: int, height: int) -> None:
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input video file not found")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cropped = frame[y:y+height, x:x+width]
        out.write(cropped)

    cap.release()
    out.release()