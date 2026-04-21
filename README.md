# 🚁 Drone Speed Estimation – from Monocular Video

## 📌 Abstract

This project estimates a drone’s horizontal speed over time from a monocular video using classical computer vision techniques.

The system computes inter-frame motion using two approaches:

- Lucas–Kanade Optical Flow (LK)
- ORB Feature Matching

Pixel displacement is converted into real-world speed using a fixed scaling factor.

---

## 🖼️ Input Visualization

### Original Frame (mid-video)
![Original Frame](assets/frame.jpg)

### Region of Interest (ROI)

A central region is used to focus on stable ground motion and reduce noise from surrounding areas.

![ROI Frame](assets/frame_roi.jpg)

---

## 🧠 Main Challenge

The main challenge is converting pixel displacement into real-world speed (m/s).

Since a monocular camera does not provide depth information, a fixed scale factor is used:

```python
speed = sqrt(dx**2 + dy**2) * FPS