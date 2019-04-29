from video_segment import VideoSegment
from data import DATASETS as DATASETS
from data import OUPUTS as OUPUTS
from logger import logger

dataset_idx = 0
dataset = DATASETS[dataset_idx]
video_segment = VideoSegment(dataset['video'], dataset['width'], dataset['height'])
content, ads = video_segment.get_content_ads_shots()
logger.d('content', content)
logger.d('ads', ads)
# print('content:\n%s'% content)
# print('ads:\n%s' % ads)
# video_segment.save_content(OUPUTS[dataset_idx])