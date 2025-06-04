import cv2
import os

def add_watermark(
    video_path: str,
    output_path: str,
    watermark_text: str = "Sample Watermark",
    font_scale: float = 1.0,
    font_thickness: int = 2,
    position: tuple = (30, 30),
    color: tuple = (255, 255, 255)
) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found.")

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_SIMPLEX

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(
            frame,
            watermark_text,
            position,
            font,
            font_scale,
            color,
            font_thickness,
            cv2.LINE_AA
        )

        out.write(frame)

    cap.release()
    out.release()

    return output_path