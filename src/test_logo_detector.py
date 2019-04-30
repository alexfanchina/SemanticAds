import numpy as np
import pickle
import path_util

from video_io import VideoIO
from logo_detector import LogoDetector
from PIL import Image
from data import DATASETS as DATASETS
from data import BRANDS
from logger import logger

logger.set_level('i')

# initializing
dataset_idx = 0
dataset = DATASETS[dataset_idx]
brands_to_detect = {k: BRANDS[k]['logo'] for k in dataset['brands_to_detect']}
video_io = VideoIO(dataset['video'], dataset['width'], dataset['height'])

# detect
logo_detector = LogoDetector(brands_to_detect)
logo_data_in_video = []
while video_io.get_next_frame_idx() < video_io.get_num_frames():
    frame_idx = video_io.get_next_frame_idx()
    logger.d('Detecting logo in %d' % frame_idx)
    pil_image = video_io.read_frame()
    brand_areas = logo_detector.detect(pil_image)
    if len(brand_areas) == 0:
        logger.i('Frame[%d]: no logo detected' % frame_idx)
    else:
        for logo_name, logo_poly in brand_areas:
            logger.i('Frame[%d]: logo [%s] at area %s' % (
                frame_idx, logo_name, logo_poly.tolist()))
            logo_data_in_video.append(
                (frame_idx, logo_name, logo_poly.tolist()))
    video_io.skip_frame(1)
logo_data_path = path_util.get_video_logo_data_path(dataset['video'])
pickle.dump(logo_data_in_video, open(logo_data_path, 'wb'))
