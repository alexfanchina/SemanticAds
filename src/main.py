import pickle

from video_io import VideoIO
from audio_io import AudioIO
from video_segment import VideoSegment
from video_logo_detect import VideoLogoDetect
from data import DATASETS
from data import BRANDS
from data import OUPUTS
from logger import logger
import path_util


def remove_ads(dataset_idx):
    dataset = DATASETS[dataset_idx]
    video_input = dataset['video']
    audio_input = dataset['audio']
    width = dataset['width']
    height = dataset['height']
    outputs = OUPUTS[dataset_idx]['no_ads']
    video_output = outputs['video']
    audio_output = outputs['audio']
    video_segment = VideoSegment(video_input, width, height)
    content, ads = video_segment.get_content_ads_shots()
    logger.d('content', content)
    logger.d('ads', ads)
    video_segment.save_content(video_output, audio_input, audio_output)

def detect_and_insert_ads(dataset_idx):
    dataset = DATASETS[dataset_idx]
    brands_to_detect = {k: BRANDS[k] for k in dataset['brands_to_detect']}
    inputs = OUPUTS[dataset_idx]['no_ads']
    outputs = OUPUTS[dataset_idx]['new_ads']
    video_input = inputs['video']
    audio_input = inputs['audio']
    width = dataset['width']
    height = dataset['height']
    video_output = outputs['video']
    audio_output = outputs['audio']
    video_logo_detect = VideoLogoDetect(video_input, width, height, brands_to_detect)
    video_logo_detect.generate_video_with_ads(video_output, audio_input, audio_output)


if __name__ == "__main__":
    logger.set_level('i')
    dataset = 2
    # remove_ads(dataset)
    detect_and_insert_ads(dataset)
