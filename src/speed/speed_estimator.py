import numpy as np

def compute_speed(dx, dy, fps):
    distance = np.sqrt(dx**2 + dy**2)
    return distance * fps