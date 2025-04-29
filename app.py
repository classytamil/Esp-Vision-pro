import streamlit as st 
import cv2
import numpy as np
import time
from ultralytics import YOLO


# -------------------- Setup --------------------
st.set_page_config(page_title="ESP32-CAM Stream", layout="centered")
model = YOLO("yolov8s.pt")  # Replace with your model path if needed

# -------------------- Session State Init --------------------
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "ip_address" not in st.session_state:
    st.session_state["ip_address"] = ""
if "selected_mode" not in st.session_state:
    st.session_state["selected_mode"] = ""
if "streaming" not in st.session_state:
    st.session_state["streaming"] = False

# -------------------- Step 1: IP and Mode Selection --------------------
if st.session_state["step"] == 1:
    st.title("📷 ESP32-CAM Stream Setup")
    st.markdown("### Step 1: Enter IP Address and Select Stream Mode")
    
    st.text_input("Enter ESP32-CAM IP Address (e.g., 192.168.1.48):", "192.168.1.48", key="ip_input_field")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 View Live Stream", use_container_width=True):
            ip = st.session_state.get("ip_input_field", "")
            if ip:
                st.session_state["ip_address"] = ip
                st.session_state["selected_mode"] = "live"
                st.session_state["step"] = 2
                st.rerun()
            else:
                st.warning("⚠️ Please enter the IP address before continuing.")

    with col2:
        if st.button("🤖 AI Processed Stream", use_container_width=True):
            ip = st.session_state.get("ip_input_field", "")
            if ip:
                st.session_state["ip_address"] = ip
                st.session_state["selected_mode"] = "ai"
                st.session_state["step"] = 2
                st.rerun()
            else:
                st.warning("⚠️ Please enter the IP address before continuing.")

# -------------------- Step 2: Stream Page --------------------
elif st.session_state["step"] == 2:
    st.title("📡 ESP32-CAM Live Feed")
    ip = st.session_state["ip_address"]
    mode = st.session_state["selected_mode"]
    url = f"http://{ip}/stream"

    st.success(f"✅ Connected to ESP32-CAM at {ip}")
    back = st.button("🔙 Back to Step 1")
    stop_button = st.button("🛑 Stop Stream")

    if back:
        st.session_state["step"] = 1
        st.rerun()

    # Start the stream automatically unless stopped
    if not st.session_state["streaming"]:
        st.session_state["streaming"] = True

    if st.session_state["streaming"] and not stop_button:
        cap = cv2.VideoCapture(url)
        frame_placeholder = st.empty()

        if not cap.isOpened():
            st.error("❌ Failed to open video stream. Check IP and connection.")
        else:
            while cap.isOpened() and st.session_state["streaming"] and not stop_button:
                ret, frame = cap.read()
                if not ret:
                    st.warning("⚠️ Failed to capture frame.")
                    break

                # Process frame based on selected mode
                if mode == "ai":
                    results = model(frame, verbose=False)[0]
                    frame = results.plot()

                frame_placeholder.image(frame, channels="BGR", use_column_width=True)
                time.sleep(0.05)

            cap.release()
            st.info("📴 Stream stopped.")
            st.session_state["streaming"] = False
