import os
import cv2
import numpy as np
import joblib

def classify_video(video_path: str, model_path: str, labels_path: str, frame_interval: int = 30) -> dict:
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    model = joblib.load(model_path)
    with open(labels_path, "r") as f:
        labels = [line.strip() for line in f.readlines()]

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video")

    predictions = {}
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % frame_interval == 0:
            resized = cv2.resize(frame, (64, 64))  
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            features = gray.flatten().reshape(1, -1)

            prediction = model.predict(features)[0]
            label = labels[prediction] if isinstance(prediction, int) else prediction
            predictions[label] = predictions.get(label, 0) + 1

        frame_id += 1

    cap.release()
    return dict(sorted(predictions.items(), key=lambda item: item[1], reverse=True))