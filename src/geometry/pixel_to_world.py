import numpy as np

def estimate_displacement(prev_pts, next_pts, status, config):
    # Handle cases where tracking failed
    if next_pts is None or status is None:
        return 0.0, 0.0

    # Reshape points to (N, 2)
    prev_pts = prev_pts.reshape(-1, 2)
    next_pts = next_pts.reshape(-1, 2)
    status = status.flatten()

    # Keep only successfully tracked points
    valid_prev = prev_pts[status == 1]
    valid_next = next_pts[status == 1]

    # Not enough points → unreliable estimation
    if len(valid_prev) < 5:
        return 0.0, 0.0

    # Compute displacement for each point
    diff = valid_next - valid_prev

    # Compute motion magnitude per point
    magnitude = np.linalg.norm(diff, axis=1)

    if len(magnitude) == 0:
        return 0.0, 0.0

    # Additional outlier filtering based on displacement magnitude
    # Keep the 90% smallest motions (remove extreme values)
    threshold = np.percentile(magnitude, 90)
    mask = magnitude < threshold

    filtered_diff = diff[mask]

    if len(filtered_diff) == 0:
        return 0.0, 0.0

    # Use median for robust estimation (less sensitive to noise)
    dx = np.median(filtered_diff[:, 0]) * config.pixel_to_meter
    dy = np.median(filtered_diff[:, 1]) * config.pixel_to_meter

    return dx, dy