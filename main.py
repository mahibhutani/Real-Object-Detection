import cv2
import os
import numpy as np
from ultralytics import YOLO

from database.db_manager import initialize_database, save_event

# ================= CONFIGURATION =================

VIDEO_PATH = "data/input_videos/video_2026-11-22_01-04-10.mp4"
OUTPUT_PATH = "outputs/processed_videos/visionguard_output.mp4"

CONFIDENCE = 0.35
LOITERING_SECONDS = 10

# Restricted zone coordinates
ZONE = [(900, 550), (1300, 550), (1300, 900), (950, 900)]

# =================================================


def point_inside_zone(point, polygon):
    return cv2.pointPolygonTest(
        np.array(polygon, dtype=np.int32),
        point,
        False
    ) >= 0


def main():

    initialize_database()

    os.makedirs("outputs/processed_videos", exist_ok=True)

    model = YOLO("yolo11n.pt")

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if fps <= 0:
        fps = 30

    writer = cv2.VideoWriter(
        OUTPUT_PATH,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    loiter_start = {}
    zone_logged = set()
    loiter_logged = set()

    frame_number = 0

    print("VisionGuard AI started.")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1
        timestamp = frame_number / fps

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=CONFIDENCE,
            verbose=False
        )

        result = results[0]

        # Draw restricted zone
        cv2.polylines(
            frame,
            [np.array(ZONE, dtype=np.int32)],
            True,
            (0, 0, 255),
            2
        )

        if result.boxes is not None and result.boxes.id is not None:

            boxes = result.boxes.xyxy.cpu().numpy()
            ids = result.boxes.id.cpu().numpy().astype(int)
            classes = result.boxes.cls.cpu().numpy().astype(int)

            for box, object_id, cls in zip(boxes, ids, classes):

                x1, y1, x2, y2 = map(int, box)
                label = model.names[cls]

                if label != "person":
                    continue

                center = ((x1 + x2) // 2, y2)

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Person ID: {object_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                # Restricted Zone Detection

                if point_inside_zone(center, ZONE):

                    if object_id not in zone_logged:

                        save_event(
                            "Restricted Zone Intrusion",
                            int(object_id),
                            f"{timestamp:.2f}",
                            "Person entered restricted area"
                        )

                        zone_logged.add(object_id)

                        print(f"Intrusion detected: ID {object_id}")

                # Loitering Detection

                if object_id not in loiter_start:
                    loiter_start[object_id] = timestamp

                duration = timestamp - loiter_start[object_id]

                if duration >= LOITERING_SECONDS:

                    if object_id not in loiter_logged:

                        save_event(
                            "Loitering",
                            int(object_id),
                            f"{timestamp:.2f}",
                            "Person remained in monitored video"
                        )

                        loiter_logged.add(object_id)

                        print(f"Loitering detected: ID {object_id}")

        writer.write(frame)

    cap.release()
    writer.release()

    print("\nProcessing completed.")
    print("Output saved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()