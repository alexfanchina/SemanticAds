from video_segment import VideoSegment
from data import DATASETS as DATASETS

dataset_idx = 0
dataset = DATASETS[dataset_idx]
video_segment = VideoSegment(dataset['video'], dataset['width'], dataset['height'])
content, ads = video_segment.get_content_ads_shots()
print('content:\n%s'% content)
print('ads:\n%s' % ads)
