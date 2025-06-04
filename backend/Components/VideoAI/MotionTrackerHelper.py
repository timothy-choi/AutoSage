import cv2
import os

def track_motion(video_path: str, output_path: str = "motion_tracked_output.mp4") -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fg_mask = back_sub.apply(frame)

        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) < 500:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()
    return output_path