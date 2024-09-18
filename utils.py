import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Extract frames from the video
def extract_frames(video_path, output_dir, frame_rate=30):
    video = cv2.VideoCapture(video_path)
    count = 0
    frame_count = 0
    success = True

    while success:
        success, frame = video.read()
        if frame_count % frame_rate == 0:
            output_path = os.path.join(output_dir, f"frame{count}.jpg")
            cv2.imwrite(output_path, frame)
            count += 1
        frame_count += 1
    video.release()

# Detect deepfake from the video frames
def detect_deepfake(video_path, model_path):
    model = load_model(model_path)
    frames_dir = 'temp_frames/'
    
    # Ensure the directory exists
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    # Extract frames
    extract_frames(video_path, frames_dir)
    
    results = {}
    for frame_file in os.listdir(frames_dir):
        frame_path = os.path.join(frames_dir, frame_file)
        img = load_img(frame_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        prediction = model.predict(img_array)
        results[frame_file] = "deepfake" if prediction > 0.5 else "real"
    
    return results
