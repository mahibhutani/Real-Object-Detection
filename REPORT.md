
# VisionGuard AI
## Intelligent Video Surveillance & Event Monitoring System

**Project Report**

---

## Abstract

VisionGuard AI is a prototype intelligent video surveillance system developed using computer vision and deep learning techniques. The system aims to automate selected surveillance tasks by detecting people in video footage, tracking their movement across frames, and identifying potential security events within predefined restricted areas.

The project integrates the YOLO11n object detection model with ByteTrack for multi-object tracking. OpenCV is used for video processing and annotation, while SQLite provides event storage. A Streamlit-based dashboard presents event statistics, detection logs, processed surveillance video, and event analytics.

The prototype demonstrates the integration of object detection, tracking, event monitoring, database management, and visualization within a modular software architecture. Functional testing was performed on sample surveillance footage to verify the operation of the implemented components.

The system is a prototype and requires further validation using larger datasets and more rigorous evaluation methods before deployment in real-world surveillance environments.

---

# 1. Introduction

## 1.1 Background

Video surveillance plays an important role in security monitoring across public spaces, institutions, commercial environments, and residential areas. Traditional surveillance systems generally require operators to continuously monitor video feeds, which can be challenging when multiple cameras or long-duration recordings are involved.

Computer vision and deep learning have made it possible to automate selected surveillance tasks, including object detection, tracking, and event monitoring.

VisionGuard AI explores the application of these techniques in a prototype surveillance system that processes video footage, detects people, tracks their movement, and records potential security events.

## 1.2 Problem Statement

Traditional video surveillance often relies on manual observation. Continuous monitoring of video streams may lead to missed events, delayed responses, and difficulties in reviewing large amounts of recorded footage.

There is a need to explore automated systems that can detect people, monitor predefined areas, record potential events, and provide visual summaries to support surveillance monitoring.

VisionGuard AI addresses this problem by integrating computer vision-based detection, tracking, event logging, and dashboard visualization into a unified prototype.

## 1.3 Objectives

The main objectives of the project are:

- To detect people in surveillance video using a deep learning model.
- To track detected individuals across video frames.
- To monitor configured restricted zones.
- To record potential restricted-zone intrusion events.
- To implement a prototype loitering-event mechanism.
- To store event information in a structured database.
- To visualize processed video and event information through a web dashboard.

## 1.4 Scope

The project focuses on processing prerecorded surveillance video and demonstrating selected surveillance-monitoring functionalities.

The implemented prototype includes person detection, tracking, restricted-zone monitoring, event logging, processed-video generation, and dashboard visualization.

The system is currently designed as an academic prototype rather than a production-ready surveillance solution.

---

# 2. Literature and Technical Background

## 2.1 Computer Vision

Computer vision is a field of artificial intelligence that enables computers to extract information from visual data such as images and videos.

In surveillance applications, computer vision techniques can be used to detect objects, identify their locations, track movement, and analyze video frames.

VisionGuard AI uses computer vision techniques to process video frames and identify people for subsequent tracking and event analysis.

## 2.2 Object Detection

Object detection is the process of identifying and locating objects within an image or video frame.

The output of an object detection model generally includes:

- Object class
- Bounding box coordinates
- Confidence score

VisionGuard AI uses YOLO11n to detect people in surveillance video frames.

## 2.3 YOLO11n

YOLO11n is a lightweight variant of the YOLO11 object detection model family.

YOLO-based models perform object detection through a single inference pipeline, making them suitable for applications requiring efficient visual processing.

The YOLO11n model is used in this project to detect people in video frames and generate bounding boxes around detected instances.

## 2.4 Object Tracking

Object tracking involves associating detected objects across successive video frames.

Tracking allows a system to maintain identities for detected objects during video processing, enabling movement monitoring and event analysis.

VisionGuard AI uses ByteTrack to associate detections across frames and assign tracking IDs.

## 2.5 ByteTrack

ByteTrack is a multi-object tracking algorithm that associates object detections across video frames.

It uses detection confidence information during the association process to improve object tracking.

In this project, ByteTrack is used through the Ultralytics tracking interface to maintain track IDs for detected people.

## 2.6 OpenCV

OpenCV is an open-source computer vision library used for image and video processing.

In VisionGuard AI, OpenCV is used for:

- Reading video frames.
- Accessing video properties.
- Drawing bounding boxes.
- Displaying tracking IDs.
- Visualizing restricted zones.
- Generating processed video output.

## 2.7 SQLite

SQLite is a lightweight relational database management system that stores data in a local database file.

The project uses SQLite to store event records containing event type, object ID, timestamp, and event details.

## 2.8 Streamlit

Streamlit is a Python framework used to develop interactive web applications.

The project uses Streamlit to create a dashboard that presents surveillance event statistics, event logs, processed video, and analytics.

---

# 3. Proposed System

## 3.1 Overview

VisionGuard AI is designed as a modular video-processing and event-monitoring system.

The system accepts surveillance video as input and processes it frame by frame. Detected people are tracked across frames. The system checks tracked positions against a configured restricted zone and records potential events.

The recorded events are stored in SQLite and displayed through a Streamlit dashboard.

## 3.2 System Architecture

The system follows the following processing pipeline:

1. Input video acquisition.
2. Video frame extraction.
3. Person detection using YOLO11n.
4. Multi-object tracking using ByteTrack.
5. Restricted-zone monitoring.
6. Event recording and database storage.
7. Video annotation and output generation.
8. Dashboard visualization and analytics.

## 3.3 Architecture Components

### Input Video Module

The system accepts prerecorded surveillance video from the configured input-video directory.

### Detection Module

The YOLO11n model processes video frames and detects people.

### Tracking Module

ByteTrack associates detections across frames and assigns tracking IDs.

### Event Monitoring Module

The system checks tracked people against a configured restricted zone and records potential events.

### Database Module

SQLite stores event records for subsequent retrieval and visualization.

### Visualization Module

The processed video is annotated with bounding boxes, tracking IDs, and restricted-zone visualization.

### Dashboard Module

The Streamlit dashboard presents event statistics, event logs, video playback, and analytics.

---

# 4. Methodology

## 4.1 Video Input

The system uses prerecorded surveillance footage as its input.

The video is loaded using OpenCV's VideoCapture functionality. The system obtains video properties such as frame rate, frame dimensions, and frame count where available.

The video is subsequently processed frame by frame.

## 4.2 Frame Processing

Each frame is extracted from the input video and passed to the detection and tracking pipeline.

The system processes frames sequentially to identify people and maintain tracking information.

## 4.3 Person Detection

The YOLO11n model is used to identify people within each frame.

The model generates detection outputs containing bounding boxes, object classes, and confidence information.

The implementation focuses on person detections for surveillance monitoring.

## 4.4 Object Tracking

Detected people are passed through the tracking pipeline using ByteTrack.

The tracker attempts to associate detections across frames and assigns tracking IDs.

These IDs are used by the event-monitoring logic to associate detections with potential events.

Tracking IDs may change or be lost when objects are occluded or when detection fails.

## 4.5 Restricted-Zone Detection

A restricted zone is defined using polygon coordinates.

The system monitors the position of detected and tracked people relative to the configured polygon.

When a tracked person is identified within the restricted zone, the system can record a potential restricted-zone intrusion event.

The event record may include the event type, object ID, timestamp, and descriptive details.

## 4.6 Loitering Event Mechanism

The current prototype implements a duration-based loitering-event mechanism using tracking information.

The system monitors the duration associated with tracked identities and records a potential loitering event when the configured duration threshold is reached.

The current implementation does not reliably distinguish stationary behavior from continued movement. Therefore, the loitering mechanism is considered a prototype rather than a robust behavioral-analysis algorithm.

## 4.7 Event Logging

Potential events are stored in a SQLite database.

The event database stores fields such as:

- Event ID
- Event type
- Object ID
- Timestamp
- Event details

The stored records are retrieved for displaying event logs and statistics in the dashboard.

## 4.8 Video Annotation

The processed video contains visual annotations generated during processing.

These annotations include:

- Bounding boxes around detected people.
- Tracking IDs.
- Restricted-zone visualization.
- Event-related visual information where implemented.

The annotated video is saved in the processed-video output directory.

## 4.9 Dashboard Visualization

The dashboard is developed using Streamlit.

It provides an interface for reviewing the surveillance-processing output.

The dashboard contains:

- Total event statistics.
- Intrusion statistics.
- Loitering statistics.
- Unattended-object statistics.
- Processed surveillance video.
- Event logs.
- Event distribution analytics.

The dashboard retrieves event records from the database and presents them in a visual format.

---

# 5. Implementation

## 5.1 Development Environment

The system was developed using Python in Visual Studio Code.

The project uses modular Python files for detection, tracking, event processing, database management, video processing, and dashboard development.

## 5.2 Software and Libraries

| Technology | Application |
|---|---|
| Python | Core implementation |
| YOLO11n | Person detection |
| Ultralytics | Model inference and tracking interface |
| ByteTrack | Multi-object tracking |
| OpenCV | Video processing |
| NumPy | Numerical and geometric operations |
| SQLite | Event storage |
| Pandas | Event data processing |
| Streamlit | Web dashboard |
| Matplotlib / Plotly | Analytics visualization |

## 5.3 Database Implementation

SQLite is used for local event storage.

The database stores records generated during the processing of surveillance video.

Event records are retrieved and displayed in the dashboard.

## 5.4 Dashboard Implementation

The dashboard is implemented using Streamlit.

It provides event metrics, event logs, processed-video playback, and an event distribution chart.

The dashboard enables users to review the output of the surveillance-processing pipeline through a browser-based interface.

## 5.5 Output Generation

The system generates annotated video output during processing.

The generated video is stored within the processed-video directory.

Event records are stored in the SQLite database and visualized in the dashboard.

---

# 6. Testing and Evaluation

## 6.1 Evaluation Approach

Functional testing was conducted to verify the operation of the major components of VisionGuard AI.

The testing focused on whether the system performed its intended operations during sample video processing.

The evaluation was conducted using a limited number of test videos.

## 6.2 Functional Test Observations

| Test | Expected Functionality | Observation |
|---|---|---|
| Person Detection | Detect people in video frames | Bounding boxes were displayed around detected persons in processed video. |
| Object Tracking | Assign tracking IDs to detected persons | Tracking IDs were visible across processed frames. |
| Restricted-Zone Detection | Detect entry into a configured zone | Restricted-zone events were recorded in the event database during testing. |
| Loitering Detection | Generate a potential loitering event | A loitering event was recorded during the test run. |
| Event Logging | Store event type, ID, timestamp, and details | Events were displayed in the dashboard. |
| Dashboard | Display event statistics and logs | Metrics, event table, and analytics chart were displayed. |
| Video Visualization | Display processed video | Browser-compatible processed video was displayed in the dashboard. |

## 6.3 Video Performance Details

The processed video used during the performance check contained the following properties:

| Parameter | Value |
|---|---|
| Frame Rate | 30 FPS |
| Total Frames | 924 |
| Resolution | 1280 × 720 |
| Duration | Approximately 30.8 seconds |

These values represent the properties of the tested video and do not constitute model accuracy or processing-speed measurements.

## 6.4 Functional Evaluation

The functional testing demonstrated that the prototype could execute its major processing and visualization components.

The tests verified person detection, tracking, restricted-zone event recording, database retrieval, dashboard visualization, and processed-video playback.

The results indicate successful functional integration of the tested components under the sample testing conditions.

## 6.5 Limitations of Evaluation

- Testing was conducted on a limited number of videos.
- No large-scale manually annotated benchmark dataset was used.
- Detection accuracy, precision, recall, and F1-score have not been formally established.
- Tracking IDs may change or be lost under occlusion or detection failure.
- The current loitering implementation is a prototype and does not reliably distinguish stationary behavior from continued movement.
- Unattended-object detection requires further validation across multiple scenarios.
- The system has not undergone extensive real-world deployment testing.

---

# 7. Results

The prototype successfully demonstrated the integration of object detection, multi-object tracking, restricted-zone monitoring, event logging, processed-video generation, and dashboard visualization.

Person detections were displayed with bounding boxes, and tracking IDs were visualized in the processed video.

Restricted-zone events and a potential loitering event were recorded during the test run and were displayed in the event dashboard.

The dashboard presented event metrics, event logs, and event-distribution analytics.

The processed surveillance video was successfully displayed in the browser-based dashboard after video compatibility adjustments.

The results demonstrate functional integration of the implemented prototype components. They do not establish formal detection accuracy or real-world surveillance reliability.

---

# 8. Limitations

The current implementation has several limitations:

- The system was evaluated using a limited number of sample videos.
- Detection performance depends on video quality, lighting, camera perspective, and object visibility.
- Tracking IDs may change or be lost during occlusion.
- The current loitering logic is duration-based and does not reliably evaluate stationary behavior.
- Unattended-object detection requires further validation.
- Formal quantitative detection evaluation has not been conducted.
- Real-time performance across different hardware configurations has not been established.
- The system is a prototype and is not intended to replace professional surveillance infrastructure.

---

# 9. Future Scope

The project can be extended in several directions.

## 9.1 Improved Loitering Detection

Spatial movement analysis can be introduced to determine whether an individual remains within a specific region for an extended duration.

## 9.2 Unattended-Object Detection

More robust object tracking and object-person association techniques can be incorporated to identify unattended objects.

## 9.3 Real-Time Camera Integration

The system can be extended to process live camera streams rather than only prerecorded videos.

## 9.4 Automated Alerts

Automated notifications can be introduced for potential restricted-zone intrusion or other monitored events.

## 9.5 Quantitative Evaluation

The system can be evaluated using manually annotated datasets and standard metrics such as precision, recall, F1-score, and tracking performance metrics.

## 9.6 Performance Optimization

Model optimization, frame sampling, hardware acceleration, and edge deployment techniques can be explored to improve processing efficiency.

## 9.7 Advanced Event Analysis

Additional computer vision and machine learning methods can be explored for behavior analysis and anomaly detection.

---

# 10. Conclusion

VisionGuard AI demonstrates a prototype intelligent video surveillance system integrating object detection, multi-object tracking, restricted-zone monitoring, event logging, and dashboard visualization.

The project combines YOLO11n, ByteTrack, OpenCV, SQLite, and Streamlit to develop a modular surveillance-processing pipeline.

Functional testing demonstrated the operation of the major implemented components using sample surveillance footage.

The project provides a foundation for further development in automated surveillance monitoring, computer vision-based event analysis, and visual security systems.

Further testing, improved behavioral-analysis algorithms, and quantitative evaluation are required to enhance the reliability and applicability of the prototype.

---

# 11. References

1. Ultralytics Documentation — YOLO. https://docs.ultralytics.com/
2. OpenCV Documentation. https://docs.opencv.org/
3. ByteTrack — Multi-Object Tracking. https://github.com/ifzhang/ByteTrack
4. Streamlit Documentation. https://docs.streamlit.io/
5. SQLite Documentation. https://www.sqlite.org/docs.html
6. NumPy Documentation. https://numpy.org/doc/
7. Pandas Documentation. https://pandas.pydata.org/docs/
