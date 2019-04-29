import numpy as np

from data import DATASETS as DATASETS
from data import BRANDS_LOGO as BRANDS
from video_io import VideoIO
from logo_detector import LogoDetector
from PIL import Image

# initializing
dataset_idx = 1
logo_name = 'mcdonalds'
dataset = DATASETS[dataset_idx]
logo_frame = dataset['brand_frames'][logo_name]
logo_path = BRANDS[logo_name]

# get image
video_io = VideoIO(dataset['video'], dataset['width'], dataset['height'])
pil_image = video_io.seek_frame(logo_frame).convert('RGB')

# detect
logo_detector = LogoDetector(pil_image)
logo_detector.detect_sift(logo_path)


