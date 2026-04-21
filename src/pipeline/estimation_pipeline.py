import csv

from src.config.config import config
from src.video.video_reader import read_video
from src.tracking.feature_tracker import detect_features
from src.motion.optical_flow import compute_optical_flow
from src.geometry.pixel_to_world import estimate_displacement
from src.motion.orb_motion import compute_orb_displacement
from src.speed.speed_estimator import compute_speed


def run_pipeline():
    frames, fps = read_video(config.video_path)

    prev_gray = None
    prev_pts = None

    results = []

    for i, gray in enumerate(frames):

        if prev_gray is None:
            prev_gray = gray
            prev_pts = detect_features(gray, config)
            continue

        # === Lucas-Kanade ===
        next_pts, status = compute_optical_flow(prev_gray, gray, prev_pts)
        dx_lk, dy_lk = estimate_displacement(prev_pts, next_pts, status, config)
        speed_lk = compute_speed(dx_lk, dy_lk, fps)

        # === ORB ===
        dx_orb, dy_orb = compute_orb_displacement(prev_gray, gray, config)
        speed_orb = compute_speed(dx_orb, dy_orb, fps)

        results.append([
            i,
            i / fps,
            speed_lk,
            speed_orb
        ])

        # === feature re-detection ===
        if next_pts is None or status is None or status.sum() < 20:
            prev_pts = detect_features(gray, config)
        else:
            prev_pts = next_pts

        prev_gray = gray

    _save_results(results, config.output_path)


def _save_results(results, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)

        # === Title ===
        writer.writerow(["=== Drone Speed Estimation Results ==="])
        writer.writerow([])

        # === Headers ===
        writer.writerow([
            "Frame Index",
            "Time (seconds)",
            "Speed LK (m/s)",
            "Speed ORB (m/s)",
            "Note"
        ])

        # === Data ===
        for frame, time, lk, orb in results:

            note = ""
            if lk == 0 or orb == 0:
                note = "Tracking lost"

            writer.writerow([frame, time, lk, orb, note])

        # === Empty line ===
        writer.writerow([])
        writer.writerow(["=== Summary ==="])

        # === Summary ===
        final_frame, final_time, final_lk, final_orb = results[-1]

        avg_lk = sum(r[2] for r in results) / len(results)
        avg_orb = sum(r[3] for r in results) / len(results)

        writer.writerow(["Final Frame", final_frame])
        writer.writerow(["Final Time (s)", final_time])
        writer.writerow(["Final Speed LK (m/s)", final_lk])
        writer.writerow(["Final Speed ORB (m/s)", final_orb])
        writer.writerow([])
        writer.writerow(["Average Speed LK (m/s)", avg_lk])
        writer.writerow(["Average Speed ORB (m/s)", avg_orb])

    print(f" CSV saved to {path}")