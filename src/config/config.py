from dataclasses import dataclass

@dataclass
class Config:
    video_path: str = "data/input/drone_video.mp4"
    output_path: str = "data/output/speed_results.csv"
    max_corners: int = 200
    quality_level: float = 0.3
    min_distance: int = 7
    pixel_to_meter: float = 0.05

config = Config()