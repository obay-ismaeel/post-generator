import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import cv2
import numpy as np

app = FastAPI()

# Frame processing functions (unchanged)
def calculate_brightness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])  # V channel in HSV represents brightness
    return brightness

def calculate_sharpness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = laplacian.var()  # Variance of the Laplacian indicates sharpness
    return sharpness

def calculate_colorfulness(frame):
    (B, G, R) = cv2.split(frame)
    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)
    colorfulness = np.mean(rg) + np.mean(yb)
    return colorfulness

def calculate_frame_difference(frame1, frame2):
    mse = np.mean((frame1.astype("float") - frame2.astype("float")) ** 2)
    return mse

async def extract_top_frames_from_video(video_file):
    current_directory = os.getcwd()
    output_folder = os.path.join(current_directory, 'output')

    interval = 1
    top_n = 3
    similarity_threshold = 1000

    cap = cv2.VideoCapture(video_file)
    count = 0
    top_frames = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    while True:
        success, frame = cap.read()
        if not success:
            break

        if count % (interval * int(cap.get(cv2.CAP_PROP_FPS))) == 0:
            brightness = calculate_brightness(frame)
            sharpness = calculate_sharpness(frame)
            colorfulness = calculate_colorfulness(frame)
            
            score = brightness + sharpness + colorfulness
            
            is_significantly_different = True
            for existing_frame, _ in top_frames:
                if calculate_frame_difference(existing_frame, frame) < similarity_threshold:
                    is_significantly_different = False
                    break

            if is_significantly_different:
                top_frames.append((frame, score))
                top_frames = sorted(top_frames, key=lambda x: x[1], reverse=True)[:top_n]

        count += 1
    
    cap.release()

    frame_paths = []
    for _, (frame, score) in enumerate(top_frames):
        unique_id = str(uuid.uuid4())
        frame_path = os.path.join(output_folder, f"top_frame_{unique_id}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
        print(f"Top frame {unique_id} saved as {frame_path}")

    return frame_paths
