import cv2


def compute_optical_flow(prev_gray, curr_gray, prev_pts):
    if prev_pts is None:
        return None, None

    next_pts, status, _ = cv2.calcOpticalFlowPyrLK(
        prev_gray,
        curr_gray,
        prev_pts,
        None
    )

    return next_pts, status