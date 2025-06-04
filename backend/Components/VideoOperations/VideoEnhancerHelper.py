import cv2
import os

def enhance_video(
    input_path: str,
    output_path: str,
    brightness: int = 30,
    contrast: int = 30
) -> str:
    if not os.path.exists(input_path):
        raise FileNotFoundError("Video not found")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        enhanced = cv2.convertScaleAbs(frame, alpha=1 + contrast / 100.0, beta=brightness)
        out.write(enhanced)

    cap.release()
    out.release()
    return output_path