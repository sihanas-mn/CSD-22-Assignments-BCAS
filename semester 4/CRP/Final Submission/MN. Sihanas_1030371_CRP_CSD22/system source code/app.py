"""
Traffic Sign Detection System using YOLOv8
A Streamlit web application for detecting and marking traffic signs in uploaded videos
"""

import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from pathlib import Path
import time
from ultralytics import YOLO
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Traffic Sign Detection System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #ff6b6b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ecdc4;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #80808;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4ecdc4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #80808;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1edff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0084ff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model(model_path):
    """Load the YOLOv8 model and cache it for performance."""
    try:
        if not os.path.exists(model_path):
            st.error(f"Model file not found at: {model_path}")
            st.stop()
        
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.stop()

def process_video(uploaded_file, model, confidence_threshold=0.5):
    """Process uploaded video and detect traffic signs."""
    
    # Create temporary file for uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # Open video capture
    cap = cv2.VideoCapture(tmp_path)
    
    if not cap.isOpened():
        st.error("Error: Could not open video file.")
        os.unlink(tmp_path)
        return None, None
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Prepare output video
    output_path = tmp_path.replace('.mp4', '_processed.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Detection statistics
    detection_stats = {
        'frame_number': [],
        'detections_count': [],
        'confidence_scores': [],
        'class_names': []
    }
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    frame_count = 0
    total_detections = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run YOLO detection
            results = model(frame, conf=confidence_threshold)
            
            # Process detections
            frame_detections = 0
            frame_confidences = []
            frame_classes = []
            
            # Draw bounding boxes and labels
            annotated_frame = results[0].plot()
            
            if results[0].boxes is not None:
                for box in results[0].boxes:
                    frame_detections += 1
                    total_detections += 1
                    
                    # Get confidence and class
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    
                    frame_confidences.append(confidence)
                    frame_classes.append(class_name)
            
            # Store frame statistics
            detection_stats['frame_number'].append(frame_count)
            detection_stats['detections_count'].append(frame_detections)
            detection_stats['confidence_scores'].append(frame_confidences)
            detection_stats['class_names'].append(frame_classes)
            
            # Write processed frame
            out.write(annotated_frame)
            
            # Update progress
            progress = frame_count / total_frames
            progress_bar.progress(progress)
            status_text.text(f"Processing frame {frame_count}/{total_frames} - Detections: {total_detections}")
            
            frame_count += 1
        
        # Clean up
        cap.release()
        out.release()
        
        # Remove temporary input file
        os.unlink(tmp_path)
        
        return output_path, detection_stats
        
    except Exception as e:
        cap.release()
        out.release()
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
        st.error(f"Error processing video: {str(e)}")
        return None, None

def display_detection_statistics(stats):
    """Display detection statistics and analytics."""
    
    if not stats['frame_number']:
        st.warning("No detection statistics available.")
        return
    
    # Create DataFrame for analysis
    data = []
    for i, frame_num in enumerate(stats['frame_number']):
        if stats['detections_count'][i] > 0:
            for j, conf in enumerate(stats['confidence_scores'][i]):
                data.append({
                    'Frame': frame_num,
                    'Detection_Count': stats['detections_count'][i],
                    'Confidence': conf,
                    'Class': stats['class_names'][i][j]
                })
    
    if not data:
        st.warning("No detections found in the video.")
        return
    
    df = pd.DataFrame(data)
    
    # Summary statistics
    total_detections = len(df)
    unique_classes = df['Class'].nunique()
    avg_confidence = df['Confidence'].mean()
    frames_with_detections = df['Frame'].nunique()
    
    # Display summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Detections", total_detections)
    with col2:
        st.metric("Unique Sign Types", unique_classes)
    with col3:
        st.metric("Avg Confidence", f"{avg_confidence:.2f}")
    with col4:
        st.metric("Frames w/ Detections", frames_with_detections)
    
    # Class distribution
    st.subheader("📊 Detection Distribution")
    class_counts = df['Class'].value_counts()
    st.bar_chart(class_counts)
    
    # Confidence distribution
    st.subheader("📈 Confidence Score Distribution")
    
    # Create histogram using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['Confidence'], bins=20, color='lightblue', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Confidence Score')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Confidence Scores')
    ax.axvline(df['Confidence'].mean(), color='red', linestyle='--', 
              label=f'Mean: {df["Confidence"].mean():.3f}')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    
    # Detailed statistics table
    st.subheader("📋 Detailed Detection Statistics")
    
    # Group by class for summary
    class_summary = df.groupby('Class').agg({
        'Confidence': ['count', 'mean', 'min', 'max'],
        'Frame': 'nunique'
    }).round(3)
    
    class_summary.columns = ['Count', 'Avg_Confidence', 'Min_Confidence', 'Max_Confidence', 'Frames_Appeared']
    st.dataframe(class_summary)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🚦 Traffic Sign Detection System</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Upload a video to detect and analyze traffic signs using YOLOv8</p>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.markdown('<h2 class="sub-header">⚙️ Configuration</h2>', unsafe_allow_html=True)
    
    # Model path input
    model_path = st.sidebar.text_input(
        "Model Path", 
        value="last_model_20250730_055459.pt",
        help="Path to your trained YOLOv8 model file"
    )
    
    # Confidence threshold
    confidence_threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.1,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Minimum confidence score for detections"
    )
    
    # Load model
    st.sidebar.markdown('<div class="info-box">Loading YOLOv8 model...</div>', unsafe_allow_html=True)
    model = load_model(model_path)
    st.sidebar.success("✅ Model loaded successfully!")
    
    # Display model information
    with st.sidebar.expander("📝 Model Information"):
        st.write(f"**Model Type:** {type(model).__name__}")
        st.write(f"**Classes:** {len(model.names)}")
        st.write("**Detected Classes:**")
        for i, class_name in model.names.items():
            st.write(f"  - {i}: {class_name}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">📹 Video Upload</h2>', unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload a video file containing traffic scenes"
        )
        
        if uploaded_file is not None:
            # Display video info
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**File size:** {uploaded_file.size / (1024*1024):.2f} MB")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Process button
            if st.button("🚀 Start Detection", type="primary"):
                st.markdown('<h3 class="sub-header">⚡ Processing Video...</h3>', unsafe_allow_html=True)
                
                with st.spinner("Detecting traffic signs..."):
                    output_path, stats = process_video(uploaded_file, model, confidence_threshold)
                
                if output_path and os.path.exists(output_path):
                    st.success("✅ Video processing completed!")
                    
                    # Display processed video
                    st.markdown('<h3 class="sub-header">🎬 Processed Video</h3>', unsafe_allow_html=True)
                    
                    with open(output_path, 'rb') as video_file:
                        video_bytes = video_file.read()
                        st.video(video_bytes)
                    
                    # Download button for processed video
                    st.download_button(
                        label="📥 Download Processed Video",
                        data=video_bytes,
                        file_name=f"processed_{uploaded_file.name}",
                        mime="video/mp4"
                    )
                    
                    # Display statistics
                    st.markdown('<h3 class="sub-header">📊 Detection Analytics</h3>', unsafe_allow_html=True)
                    display_detection_statistics(stats)
                    
                    # Clean up temporary file
                    try:
                        os.unlink(output_path)
                    except:
                        pass
                else:
                    st.error("❌ Failed to process video. Please try again.")
    
    with col2:
        st.markdown('<h2 class="sub-header">💡 Instructions</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h4>How to use:</h4>
        <ol>
            <li>Ensure your <code>best.pt</code> model file is in the same directory</li>
            <li>Adjust the confidence threshold if needed</li>
            <li>Upload a video file containing traffic scenes</li>
            <li>Click "Start Detection" to process</li>
            <li>View results and download processed video</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
        <h4>⚠️ Important Notes:</h4>
        <ul>
            <li>Larger videos will take more time to process</li>
            <li>Ensure good lighting and clear view of signs</li>
            <li>Supported formats: MP4, AVI, MOV, MKV</li>
            <li>Processing time depends on video length and complexity</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # System information
        with st.expander("🖥️ System Information"):
            import torch
            st.write(f"**Python Version:** {st.__version__}")
            st.write(f"**PyTorch Version:** {torch.__version__}")
            st.write(f"**CUDA Available:** {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                st.write(f"**GPU:** {torch.cuda.get_device_name(0)}")

    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Traffic Sign Detection System | Powered by YOLOv8 & Streamlit</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
