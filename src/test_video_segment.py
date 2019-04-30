import numpy as np
from test_data import DATASETS as DATASETS
from test_data import EXPECTED_SEGMENTS as EXPECTED
from video_segment import VideoSegment
from logger import logger

def in_shots(s, shots):
    if type(shots) is tuple:
        return s[0] >= shots[0] and s[1] <= shots[1]
    else:
        result = False
        for shot in shots:
            result = result or in_shots(s, shot)
        return result

def get_expected_indices(segment_shots, expected_contents):
    content_indices = []
    ads_indices = []
    for i, shot in enumerate(segment_shots):
        if in_shots(shot, expected_contents):
            content_indices.append(i)
        else:
            ads_indices.append(i)
    return np.array(content_indices), np.array(ads_indices)

dataset_idx = 0
dataset = DATASETS[dataset_idx]
video_segment = VideoSegment(dataset['video'], dataset['width'], dataset['height'])
content, ads = video_segment.get_content_ads_shots()

content_expected, ads_expected = get_expected_indices(
    video_segment.get_all_shots(), EXPECTED[dataset_idx]['content_shots'])
logger.d('shots', np.array(video_segment.get_all_shots()))
logger.d('content', video_segment.content_shots)
logger.d('content_expected', content_expected)
logger.d('ads', video_segment.ads_shots)
logger.d('ads_expected', ads_expected)
