import cv2
import numpy as np


def compute_orb_displacement(prev_gray, curr_gray, config):
    # === ORB detector ===
    orb = cv2.ORB_create(
        nfeatures=1500
    )

    kp1, des1 = orb.detectAndCompute(prev_gray, None)
    kp2, des2 = orb.detectAndCompute(curr_gray, None)

    if des1 is None or des2 is None:
        return 0.0, 0.0

    if len(kp1) < 10 or len(kp2) < 10:
        return 0.0, 0.0

    # === KNN matching ===
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)

    # === Ratio test ===
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    if len(good) < 10:
        return 0.0, 0.0

    # === Extract matched points ===
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good])

    # === RANSAC (filter incorrect matches) ===
    H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

    if mask is None:
        return 0.0, 0.0

    inliers = mask.ravel() == 1

    pts1 = pts1[inliers]
    pts2 = pts2[inliers]

    if len(pts1) < 5:
        return 0.0, 0.0

    # === Compute displacement ===
    diff = pts2 - pts1

    # Additional outlier filtering based on displacement magnitude
    magnitude = np.linalg.norm(diff, axis=1)
    threshold = np.percentile(magnitude, 90)
    diff = diff[magnitude < threshold]

    if len(diff) == 0:
        return 0.0, 0.0

    # Use median for robust estimation
    dx = np.median(diff[:, 0]) * config.pixel_to_meter
    dy = np.median(diff[:, 1]) * config.pixel_to_meter

    return dx, dy