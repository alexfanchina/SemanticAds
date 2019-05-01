import pickle

from video_segment import VideoSegment
from video_io import VideoIO
from logo_detector import LogoDetector
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
    brands_to_detect = {k: BRANDS[k]['logo']
                        for k in dataset['brands_to_detect']}
    inputs = OUPUTS[dataset_idx]['no_ads']
    outputs = OUPUTS[dataset_idx]['new_ads']
    video_input = inputs['video']
    audio_input = inputs['audio']
    width = dataset['width']
    height = dataset['height']
    video_output = outputs['video']
    audio_output = outputs['audio']

    video_io = VideoIO(video_input, width, height)
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
    logo_data_path = path_util.get_video_logo_data_path(video_input)
    pickle.dump(logo_data_in_video, open(logo_data_path, 'wb'))
    # TODO


if __name__ == "__main__":
    dataset = 0
    remove_ads(dataset)
