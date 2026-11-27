import os
import tempfile
import subprocess
from collections import Counter

import cv2
import pandas as pd
import streamlit as st
from ultralytics import YOLO

from database.db_manager import get_events


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="VisionGuard AI",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ VisionGuard AI")
st.caption("Intelligent Video Surveillance & Event Monitoring")


# --------------------------------------------------
# MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")


# --------------------------------------------------
# HISTORICAL DATABASE DASHBOARD
# --------------------------------------------------
events = get_events()
columns = ["ID", "Event Type", "Object ID", "Timestamp", "Details"]
df = pd.DataFrame(events, columns=columns)

if not df.empty:
    df["Event Type"] = df["Event Type"].astype(str)

total_events = len(df)
intrusions = int((df["Event Type"] == "Restricted Zone Intrusion").sum()) if not df.empty else 0
loitering = int((df["Event Type"] == "Loitering").sum()) if not df.empty else 0
unattended = int((df["Event Type"] == "Potential Unattended Object").sum()) if not df.empty else 0

st.header("📊 System Event Overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Events", total_events)
m2.metric("Intrusions", intrusions)
m3.metric("Loitering", loitering)
m4.metric("Unattended Objects", unattended)


# --------------------------------------------------
# UPLOAD / ANALYZE SECTION
# --------------------------------------------------
with st.expander("🎥 Upload & Analyze Your Own Video", expanded=True):
    st.write(
        "Upload a video to detect and track supported objects "
        "using YOLO11n and ByteTrack."
    )

    uploaded_video = st.file_uploader(
        "Choose a video file",
        type=["mp4", "avi", "mov", "mkv"],
        key="visionguard_upload",
    )

    if uploaded_video is not None:
        st.caption("Original uploaded video")
        st.video(uploaded_video.getvalue(), width=700)

        analyze_clicked = st.button(
            "🔍 Analyze Uploaded Video",
            type="primary",
            key="visionguard_analyze",
        )

        if analyze_clicked:
            st.session_state.pop("vg_analysis", None)

            progress_bar = st.progress(0)
            status_text = st.empty()

            with st.spinner("Processing video. This may take a while..."):
                temp_dir = tempfile.mkdtemp(prefix="visionguard_")
                input_path = os.path.join(temp_dir, "uploaded_input_video")
                output_path = os.path.join(temp_dir, "analyzed_video.mp4")
                browser_output_path = os.path.join(
                    temp_dir, "analyzed_video_browser.mp4"
                )

                # Save uploaded video bytes
                with open(input_path, "wb") as f:
                    f.write(uploaded_video.getvalue())

                cap = cv2.VideoCapture(input_path)
                if not cap.isOpened():
                    st.error("Unable to open the uploaded video.")
                else:
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                    if fps <= 0:
                        fps = 30.0

                    if width <= 0 or height <= 0:
                        cap.release()
                        st.error("The uploaded video has invalid frame dimensions.")
                    else:
                        writer = cv2.VideoWriter(
                            output_path,
                            cv2.VideoWriter_fourcc(*"mp4v"),
                            fps,
                            (width, height),
                        )

                        if not writer.isOpened():
                            cap.release()
                            st.error("Could not create the processed video file.")
                        else:
                            model = load_model()
                            class_counts = Counter()
                            tracked_ids = {}
                            processed_frames = 0
                            processing_error = None

                            try:
                                while True:
                                    ret, frame = cap.read()
                                    if not ret:
                                        break

                                    results = model.track(
                                        frame,
                                        persist=True,
                                        tracker="bytetrack.yaml",
                                        verbose=False,
                                    )
                                    result = results[0]
                                    annotated_frame = result.plot()
                                    writer.write(annotated_frame)

                                    boxes = result.boxes
                                    if boxes is not None and len(boxes) > 0:
                                        cls_ids = (
                                            boxes.cls.cpu()
                                            .numpy()
                                            .astype(int)
                                        )

                                        for cls_id in cls_ids:
                                            class_name = model.names[int(cls_id)]
                                            class_counts[class_name] += 1

                                        if boxes.id is not None:
                                            ids = (
                                                boxes.id.cpu()
                                                .numpy()
                                                .astype(int)
                                            )
                                            for cls_id, track_id in zip(cls_ids, ids):
                                                class_name = model.names[int(cls_id)]
                                                tracked_ids.setdefault(
                                                    class_name, set()
                                                ).add(int(track_id))

                                    processed_frames += 1
                                    if total_frames > 0:
                                        progress_bar.progress(
                                            min(processed_frames / total_frames, 1.0)
                                        )
                                    status_text.text(
                                        f"Processing frame {processed_frames}"
                                        + (f" of {total_frames}" if total_frames > 0 else "")
                                    )
                            except Exception as exc:
                                processing_error = str(exc)
                            finally:
                                cap.release()
                                writer.release()

                            if processing_error:
                                st.error(f"Video processing failed: {processing_error}")
                            elif processed_frames == 0:
                                st.error("No frames could be read from the video.")
                            else:
                                progress_bar.progress(1.0)
                                status_text.text("Processing completed.")

                                # Convert to browser-friendly H.264 if possible
                                conversion_success = False
                                try:
                                    import imageio_ffmpeg

                                    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                                    subprocess.run(
                                        [
                                            ffmpeg_path,
                                            "-y",
                                            "-i",
                                            output_path,
                                            "-vcodec",
                                            "libx264",
                                            "-pix_fmt",
                                            "yuv420p",
                                            "-acodec",
                                            "aac",
                                            browser_output_path,
                                        ],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL,
                                        check=True,
                                    )
                                    conversion_success = os.path.exists(
                                        browser_output_path
                                    )
                                except Exception:
                                    conversion_success = False

                                final_video_path = (
                                    browser_output_path
                                    if conversion_success
                                    else output_path
                                )

                                summary_df = pd.DataFrame(
                                    [
                                        {
                                            "Object Class": name,
                                            "Detection Instances": count,
                                            "Unique Tracking IDs": len(
                                                tracked_ids.get(name, set())
                                            ),
                                        }
                                        for name, count in class_counts.items()
                                    ]
                                )

                                total_detections = sum(class_counts.values())
                                total_unique_ids = sum(
                                    len(ids) for ids in tracked_ids.values()
                                )

                                report_text = (
                                    "VISIONGUARD-AI VIDEO ANALYSIS REPORT\n"
                                    "===================================\n\n"
                                    f"Frames processed: {processed_frames}\n"
                                    f"Total detection instances: {total_detections}\n"
                                    f"Total unique tracking IDs (summed across classes): "
                                    f"{total_unique_ids}\n\n"
                                    "OBJECT-WISE ANALYSIS\n"
                                    "-------------------\n"
                                )

                                for class_name, count in class_counts.items():
                                    report_text += (
                                        f"{class_name}: {count} detection instances, "
                                        f"{len(tracked_ids.get(class_name, set()))} "
                                        "unique tracking IDs\n"
                                    )

                                report_text += (
                                    "\nNOTES\n-----\n"
                                    "Detection instances represent detections across video frames.\n"
                                    "Tracking IDs are estimates generated by the tracker.\n"
                                    "This is not a formal accuracy evaluation.\n"
                                )

                                st.session_state["vg_analysis"] = {
                                    "video_path": final_video_path,
                                    "summary_df": summary_df,
                                    "report_text": report_text,
                                    "total_detections": total_detections,
                                    "total_unique_ids": total_unique_ids,
                                    "processed_frames": processed_frames,
                                    "temp_dir": temp_dir,
                                }

        # Display stored results after processing and on download-button reruns
        analysis = st.session_state.get("vg_analysis")
        if analysis:
            st.success("Video analysis completed!")

            st.subheader("🎬 Analyzed Video")
            st.video(analysis["video_path"], width=700)

            st.subheader("📦 Detection Summary")
            summary_df = analysis["summary_df"]

            if not summary_df.empty:
                st.dataframe(
                    summary_df,
                    use_container_width=True,
                    hide_index=True,
                )
                st.bar_chart(
                    summary_df.set_index("Object Class")["Detection Instances"]
                )
            else:
                st.info("No objects were detected in this video.")

            k1, k2, k3 = st.columns(3)
            k1.metric("Detection Instances", analysis["total_detections"])
            k2.metric("Unique Track IDs (summed)", analysis["total_unique_ids"])
            k3.metric("Frames Processed", analysis["processed_frames"])

            st.subheader("📥 Download Analysis Results")

            csv_data = summary_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📊 Download Analytics CSV",
                data=csv_data,
                file_name="visionguard_analytics.csv",
                mime="text/csv",
                key="vg_csv_download",
            )

            try:
                with open(analysis["video_path"], "rb") as video_file:
                    video_bytes = video_file.read()
                st.download_button(
                    "🎥 Download Annotated Video",
                    data=video_bytes,
                    file_name="visionguard_analyzed.mp4",
                    mime="video/mp4",
                    key="vg_video_download",
                )
            except OSError:
                st.warning("The processed video file is no longer available. Re-analyze it.")

            st.download_button(
                "📄 Download Analysis Report",
                data=analysis["report_text"],
                file_name="visionguard_report.txt",
                mime="text/plain",
                key="vg_report_download",
            )


# --------------------------------------------------
# PREVIOUSLY PROCESSED SURVEILLANCE VIDEO
# --------------------------------------------------
with st.expander("📹 Previously Processed Surveillance Video", expanded=False):
    video_path = "outputs/processed_videos/visionguard_browser.mp4"
    if os.path.exists(video_path):
        st.video(video_path, width=700)
    else:
        st.info("No previously processed video found.")


# --------------------------------------------------
# HISTORICAL EVENT LOGS
# --------------------------------------------------
with st.expander("🚨 Detection Event Logs", expanded=False):
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No events recorded yet.")


# --------------------------------------------------
# HISTORICAL EVENT ANALYTICS
# --------------------------------------------------
with st.expander("📈 Historical Event Analytics", expanded=False):
    if not df.empty:
        event_counts = df["Event Type"].value_counts()
        st.bar_chart(event_counts)
    else:
        st.info("No historical events to chart.")


st.divider()
st.caption("VisionGuard AI | AI-Powered Surveillance Prototype")
