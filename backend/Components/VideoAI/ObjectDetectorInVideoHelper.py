import cv2
import os

def detect_objects_in_video(
    video_path: str,
    config_path: str,
    weights_path: str,
    names_path: str,
    confidence_threshold: float = 0.5,
    nms_threshold: float = 0.4
) -> list:
    if not all(os.path.exists(p) for p in [video_path, config_path, weights_path, names_path]):
        raise FileNotFoundError("One or more input files not found.")

    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

    with open(names_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    cap = cv2.VideoCapture(video_path)
    detections = []
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255, size=(416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)

        boxes, confidences, class_ids = [], [], []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(scores.argmax())
                confidence = scores[class_id]

                if confidence > confidence_threshold:
                    center_x, center_y, w, h = (detection[0:4] * [width, height, width, height]).astype('int')
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, int(w), int(h)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
        frame_detections = [
            {
                "object": classes[class_ids[i]],
                "confidence": round(confidences[i], 2),
                "box": boxes[i]
            } for i in indices.flatten()
        ]
        detections.append({
            "frame": frame_index,
            "objects": frame_detections
        })
        frame_index += 1

    cap.release()
    return detections