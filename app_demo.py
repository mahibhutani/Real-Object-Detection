import streamlit as st
import pandas as pd
import os

from database.db_manager import get_events

st.set_page_config(
    page_title="VisionGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ VisionGuard AI")
st.subheader("Intelligent Video Surveillance & Event Monitoring")

st.markdown("---")

# Load database events
events = get_events()

columns = ["ID", "Event Type", "Object ID", "Timestamp", "Details"]

df = pd.DataFrame(events, columns=columns)

if not df.empty:
    df["Event Type"] = df["Event Type"].astype(str)

# Metrics
total_events = len(df)

intrusions = 0
loitering = 0
unattended = 0

if not df.empty:
    intrusions = (df["Event Type"] == "Restricted Zone Intrusion").sum()
    loitering = (df["Event Type"] == "Loitering").sum()
    unattended = (df["Event Type"] == "Potential Unattended Object").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", total_events)
col2.metric("Intrusions", intrusions)
col3.metric("Loitering", loitering)
col4.metric("Unattended Objects", unattended)

st.markdown("---")

# Processed Surveillance Video
st.header("📹 Processed Surveillance Video")

video_path = "outputs/processed_videos/visionguard_browser.mp4"

if os.path.exists(video_path):
    st.success("Browser-compatible processed video loaded.")
    st.video(video_path)
else:
    st.error("Converted video file not found.")

# Event logs
st.header("🚨 Detection Event Logs")

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No events recorded yet.")

st.markdown("---")

# Event distribution
st.header("📊 Event Analytics")

if not df.empty:

    event_counts = df["Event Type"].value_counts()

    st.bar_chart(event_counts)

st.markdown("---")

st.caption("VisionGuard AI | AI-Powered Surveillance Prototype")