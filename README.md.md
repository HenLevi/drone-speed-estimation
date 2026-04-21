# Drone Speed Estimation

This project estimates a drone’s horizontal speed from video using visual motion between frames.

## Approach
- Read video and extract frames (`video_reader`)
- Convert frames to grayscale  
- Detect feature points (`feature_tracker`)
- Estimate motion using:
  - Lucas-Kanade Optical Flow (`optical_flow`)
  - ORB Feature Matching (`orb_motion`)
- Compute displacement (`pixel_to_world`)
- Convert pixel movement to meters (using a scaling factor)
- Compute speed in meters per second (`speed_estimator`)
- Run the full pipeline (`estimation_pipeline`)

## Output
A CSV file (`data/output/speed_results.csv`) containing:
- Frame index  
- Time (seconds)  
- Speed (LK & ORB)  
- Notes (e.g., tracking loss)  
- Summary (final and average speeds)

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt