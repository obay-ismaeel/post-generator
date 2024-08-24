# import cv2
# import opencv_cuda
# import numpy as np
# import os
# import time

# def calculate_brightness_gpu(frame):
#     gpu_frame = cv2.cuda_GpuMat()
#     gpu_frame.upload(frame)
#     hsv = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2HSV)
#     hsv_cpu = hsv.download()
#     brightness = np.mean(hsv_cpu[:, :, 2])  # V channel in HSV represents brightness
#     return brightness

# def calculate_sharpness_gpu(frame):
#     gpu_frame = cv2.cuda_GpuMat()
#     gpu_frame.upload(frame)
#     gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
#     laplacian = cv2.cuda.Laplacian(gray, cv2.CV_64F)
#     laplacian_cpu = laplacian.download()
#     sharpness = laplacian_cpu.var()  # Variance of the Laplacian indicates sharpness
#     return sharpness

# def calculate_colorfulness_gpu(frame):
#     gpu_frame = cv2.cuda_GpuMat()
#     gpu_frame.upload(frame)
#     channels = cv2.cuda.split(gpu_frame)
#     rg = cv2.cuda.absdiff(channels[2], channels[1])
#     yb = cv2.cuda.absdiff(cv2.cuda.addWeighted(channels[2], 0.5, channels[1], 0.5, 0), channels[0])
#     rg_cpu = rg.download()
#     yb_cpu = yb.download()
#     colorfulness = np.mean(rg_cpu) + np.mean(yb_cpu)
#     return colorfulness

# def calculate_frame_difference_gpu(frame1, frame2):
#     gpu_frame1 = cv2.cuda_GpuMat()
#     gpu_frame2 = cv2.cuda_GpuMat()
#     gpu_frame1.upload(frame1)
#     gpu_frame2.upload(frame2)
#     diff = cv2.cuda.absdiff(gpu_frame1, gpu_frame2)
#     diff_cpu = diff.download()
#     mse = np.mean(diff_cpu.astype("float") ** 2)
#     return mse

# def extract_top_frames_from_video(video_name):
#     current_directory = os.getcwd()
#     output_folder = f'{current_directory}/output'
#     full_video_path = f'{current_directory}/{video_name}'

#     interval = 1
#     top_n = 3
#     similarity_threshold = 1000

#     cap = cv2.VideoCapture(full_video_path)
#     count = 0
#     top_frames = []

#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         if count % (interval * int(cap.get(cv2.CAP_PROP_FPS))) == 0:
#             # Calculate metrics using GPU-accelerated functions
#             brightness = calculate_brightness_gpu(frame)
#             sharpness = calculate_sharpness_gpu(frame)
#             colorfulness = calculate_colorfulness_gpu(frame)
            
#             # Combined score (you can adjust the weights as needed)
#             score = brightness + sharpness + colorfulness
            
#             # Check if the new frame is significantly different from the already selected top frames
#             is_significantly_different = True
#             for existing_frame, _ in top_frames:
#                 if calculate_frame_difference_gpu(existing_frame, frame) < similarity_threshold:
#                     is_significantly_different = False
#                     break

#             if is_significantly_different:
#                 # Keep track of the top N frames
#                 top_frames.append((frame, score))
#                 top_frames = sorted(top_frames, key=lambda x: x[1], reverse=True)[:top_n]

#         count += 1
    
#     cap.release()

#     # Save the top frames
#     for idx, (frame, score) in enumerate(top_frames):
#         frame_path = f"{output_folder}/top_frame_{idx+1}.jpg"
#         cv2.imwrite(frame_path, frame)
#         print(f"Top frame {idx+1} saved as {frame_path}")

# # Example usage
# video_name = 'output.mp4'

# start_time = time.time()  # Record start time
# extract_top_frames_from_video(video_name)
# end_time = time.time()  # Record end time

# elapsed_time = end_time - start_time
# print(f"Time taken: {elapsed_time:.2f} seconds")
