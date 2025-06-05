import cv2
import os

def resize_video(
    input_path: str,
    output_path: str,
    width: int,
    height: int
) -> str:
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input video not found.")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open input video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, codec, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (width, height))
        out.write(resized_frame)

    cap.release()
    out.release()
    return output_path