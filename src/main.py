from video_segment import VideoSegment
from data import DATASETS
from data import OUPUTS
from logger import logger

dataset_idx = 0
dataset = DATASETS[dataset_idx]
output = OUPUTS[dataset_idx]['no_ads']
video_segment = VideoSegment(dataset['video'], dataset['width'], dataset['height'])
content, ads = video_segment.get_content_ads_shots()
logger.d('content', content)
logger.d('ads', ads)
video_segment.save_content(output['video'], dataset['audio'], output['audio'])
