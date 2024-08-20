import cv2
import numpy as np
import os
import time

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
    # Calculate Mean Squared Error (MSE) between two frames
    mse = np.mean((frame1.astype("float") - frame2.astype("float")) ** 2)
    return mse

def extract_top_frames_from_video(video_name):

    current_directory: str = os.getcwd()
    output_folder = f'{current_directory}/output'
    full_video_path = f'{current_directory}/{video_name}'

    interval = 1
    top_n = 3
    similarity_threshold = 1000

    cap = cv2.VideoCapture(full_video_path)
    count = 0
    top_frames = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    while True:
        success, frame = cap.read()
        if not success:
            break

        if count % (interval * int(cap.get(cv2.CAP_PROP_FPS))) == 0:
            # Calculate metrics
            brightness = calculate_brightness(frame)
            sharpness = calculate_sharpness(frame)
            colorfulness = calculate_colorfulness(frame)
            
            # Combined score (you can adjust the weights as needed)
            score = brightness + sharpness + colorfulness
            
            # Check if the new frame is significantly different from the already selected top frames
            is_significantly_different = True
            for existing_frame, _ in top_frames:
                if calculate_frame_difference(existing_frame, frame) < similarity_threshold:
                    is_significantly_different = False
                    break

            if is_significantly_different:
                # Keep track of the top N frames
                top_frames.append((frame, score))
                top_frames = sorted(top_frames, key=lambda x: x[1], reverse=True)[:top_n]

        count += 1
    
    cap.release()

    # Save the top frames
    for idx, (frame, score) in enumerate(top_frames):
        frame_path = f"{output_folder}/top_frame_{idx+1}.jpg"
        cv2.imwrite(frame_path, frame)
        print(f"Top frame {idx+1} saved as {frame_path}")

# Example usage
video_name = 'output.mp4'

start_time = time.time() # Record start time
extract_top_frames_from_video(video_name)
end_time = time.time() # Record end time

elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds") 
