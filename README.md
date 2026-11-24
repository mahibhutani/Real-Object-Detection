
# VisionGuard AI
### Intelligent Video Surveillance & Event Monitoring System

VisionGuard AI is an AI-powered video surveillance prototype designed to detect people, track their movement across video frames, and identify potential security events such as restricted-zone intrusion and loitering.

The system combines computer vision, object tracking, event logging, and a web-based dashboard to visualize surveillance activity.

---

## 1. Project Overview

Traditional surveillance systems largely depend on continuous human monitoring. VisionGuard AI explores how computer vision can automate parts of this process by detecting and tracking people in video footage and recording potential security events.

The system processes surveillance video, identifies people using a YOLO object detection model, assigns tracking IDs using ByteTrack, and monitors configured restricted zones for potential intrusion events.

Detected events are stored in a SQLite database and visualized through an interactive Streamlit dashboard.

---

## 2. Objectives

- Detect people in surveillance video using deep learning.
- Track detected individuals across video frames.
- Identify potential restricted-zone intrusion events.
- Implement a prototype loitering-event mechanism.
- Store event information in a SQLite database.
- Visualize event statistics and logs through a web dashboard.
- Generate annotated surveillance videos for visualization.

---

## 3. Features

### Person Detection
Uses YOLO11n to identify people in video frames and generate bounding boxes.

### Object Tracking
Uses ByteTrack to associate detected individuals across consecutive frames and assign tracking IDs.

### Restricted-Zone Monitoring
Uses a configured polygonal region to identify when tracked people enter a restricted area.

### Loitering Event Detection
Implements a prototype duration-based mechanism for recording potential loitering events.

### Event Logging
Stores event types, object IDs, timestamps, and event details in an SQLite database.

### Interactive Dashboard
Uses Streamlit to display event metrics, event logs, processed surveillance video, and event analytics.

### Video Annotation
Generates processed videos with detection boxes, tracking IDs, and restricted-zone visualization.

---

## 4. System Architecture

The system follows a modular processing pipeline:

1. Input surveillance video
2. Frame extraction using OpenCV
3. Person detection using YOLO11n
4. Object tracking using ByteTrack
5. Restricted-zone event analysis
6. Event recording using SQLite
7. Processed video generation
8. Dashboard visualization using Streamlit

---

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLO11n | Object detection |
| Ultralytics | YOLO model implementation |
| ByteTrack | Multi-object tracking |
| OpenCV | Video processing and annotation |
| NumPy | Numerical and geometric operations |
| SQLite | Event database |
| Pandas | Data processing and event analysis |
| Streamlit | Interactive web dashboard |
| Matplotlib / Plotly | Data visualization |

---

## 6. Project Structure

```text
VisionGuard-AI/
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── REPORT.md
│
├── detection/
│   ├── __init__.py
│   ├── detector.py
│   └── tracker.py
│
├── events/
│   ├── __init__.py
│   ├── restricted_zone.py
│   ├── unattended_object.py
│   └── loitering.py
│
├── database/
│   ├── __init__.py
│   └── db_manager.py
│
├── utils/
│   ├── __init__.py
│   ├── video_utils.py
│   └── visualization.py
│
├── data/
│   ├── input_videos/
│   └── sample_dataset/
│
├── outputs/
│   ├── processed_videos/
│   ├── screenshots/
│   └── logs/
│
├── experiments/
│   ├── experiment_results.csv
│   └── evaluation.ipynb
│
└── models/
    └── README.md
```

---

## 7. Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/mahibhutani/VisionGuard-AI.git
```

Navigate to the project directory:

```bash
cd VisionGuard-AI
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

---

## 8. Running the System

### Step 1: Prepare the input video

Place your surveillance video inside:

```text
data/input_videos/
```

Update the input video path in `main.py` if required.

### Step 2: Run the detection pipeline

```bash
python main.py
```

The processing pipeline performs person detection, tracking, event analysis, event logging, and video annotation.

### Step 3: View the processed video

The generated video is saved inside:

```text
outputs/processed_videos/
```

### Step 4: Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will open in a browser, generally at:

```text
http://localhost:8501
```

---

## 9. Dashboard Components

The VisionGuard AI dashboard provides:

- Total event count
- Restricted-zone intrusion statistics
- Loitering-event statistics
- Unattended-object event statistics
- Processed surveillance video
- Detection event logs
- Event distribution analytics

---

## 10. Evaluation

The prototype was evaluated through functional testing using sample surveillance video.

The functional tests included:

- Person detection
- Object tracking
- Restricted-zone monitoring
- Loitering-event recording
- Event database logging
- Dashboard visualization
- Processed video playback

The evaluation focuses on verifying the functionality of the implemented components.

Formal detection metrics such as precision, recall, and F1-score were not established because a sufficiently annotated ground-truth dataset was not used.

---

## 11. Limitations

- The system was evaluated using a limited number of test videos.
- Detection performance may vary depending on lighting, camera angle, video quality, and occlusion.
- Tracking IDs may change or be lost during occlusion.
- The current loitering mechanism is a prototype and does not reliably distinguish stationary behavior from continued movement.
- Unattended-object detection requires further validation.
- The system has not been evaluated on a large-scale benchmark dataset.
- The current implementation is a prototype and is not intended to replace professional surveillance infrastructure.

---

## 12. Future Scope

- Improve loitering detection using spatial movement analysis.
- Implement robust unattended-object detection.
- Develop real-time camera-stream processing.
- Introduce automated alerts and notifications.
- Improve event classification and anomaly detection.
- Evaluate the system using annotated datasets.
- Implement performance optimization for real-time deployment.
- Explore edge-device deployment.

---

## 13. Conclusion

VisionGuard AI demonstrates a prototype intelligent video surveillance system integrating object detection, multi-object tracking, restricted-zone monitoring, event logging, and dashboard visualization.

The project explores the application of computer vision and AI-based monitoring techniques to automate selected surveillance tasks and provide a visual interface for reviewing potential security events.

---

## 14. Authors

Developed as an academic AI and computer vision project.

**VisionGuard AI — AI-Powered Surveillance & Event Monitoring**

