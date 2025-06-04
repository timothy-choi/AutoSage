import cv2
import os
import numpy as np

def detect_objects_in_video(video_path: str, model_cfg: str, model_weights: str, labels_path: str, confidence_threshold: float = 0.5) -> list:
    """
    Detects objects in a video using a pretrained YOLO model.

    Parameters:
        video_path (str): Path to the video file.
        model_cfg (str): Path to YOLO model configuration file.
        model_weights (str): Path to YOLO weights.
        labels_path (str): Path to file containing class labels.
        confidence_threshold (float): Minimum confidence for a detection.

    Returns:
        List[dict]: List of frames with detected objects and their labels.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    with open(labels_path, "r") as f:
        labels = [line.strip() for line in f.readlines()]

    net = cv2.dnn.readNetFromDarknet(model_cfg, model_weights)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    cap = cv2.VideoCapture(video_path)
    frame_data = []
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)

        detections = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > confidence_threshold:
                    label = labels[class_id]
                    detections.append({"label": label, "confidence": float(round(confidence, 2))})

        frame_data.append({"frame_id": frame_id, "objects": detections})
        frame_id += 1

    cap.release()
    return frame_data