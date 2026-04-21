import cv2
from pathlib import Path

VIDEO_PATH = "data/input/drone_video.mp4"
OUTPUT_DIR = "assets"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)


total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
middle_frame = total_frames // 2

cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
ret, frame = cap.read()

if not ret:
    raise Exception("Failed to read frame")

cv2.imwrite(f"{OUTPUT_DIR}/frame.jpg", frame)

cap.release()

print(" Frame saved to assets/frame.jpg")