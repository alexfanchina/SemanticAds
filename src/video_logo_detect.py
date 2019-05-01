import pickle
import numpy as np

from video_io import VideoIO
from audio_io import AudioIO
from logo_detector import LogoDetector
from logger import logger
import path_util

class VideoLogoDetect:

    SKIP_FRAME = 2

    def __init__(self, path_video_file, frame_width, frame_height, brands_to_detect):
        self.video_path = path_video_file
        self.video_reader = VideoIO(
            path_video_file, frame_width, frame_height)
        self.brands_to_detect = brands_to_detect
        brands_path = {k: brands_to_detect[k]['logo'] for k in brands_to_detect}
        self.logo_detector = LogoDetector(brands_path)
        self.logo_data_in_video = []
        self.logo_first_occurences = dict()
        self._detect()

    def _detect(self):
        """Detect logos in all frames 
        """
        while self.video_reader.get_next_frame_idx() < self.video_reader.get_num_frames():
            frame_idx = self.video_reader.get_next_frame_idx()
            logger.d('Detecting logo in %d' % frame_idx)
            pil_image = self.video_reader.read_frame()
            brand_areas = self.logo_detector.detect(pil_image)
            if len(brand_areas) == 0:
                logger.i('Frame[%d]: no logo detected' % frame_idx)
            else:
                for logo_name, logo_poly in brand_areas:
                    logger.i('Frame[%d]: logo [%s] at area %s' % (
                        frame_idx, logo_name, logo_poly.tolist()))
                    self.logo_data_in_video.append(
                        [frame_idx, logo_name, logo_poly.tolist()])
                    if logo_name not in self.logo_first_occurences:
                        self.logo_first_occurences[logo_name] = frame_idx
            self.video_reader.skip_frame(VideoLogoDetect.SKIP_FRAME)
        logo_data_path = path_util.get_video_logo_data_path(self.video_path)
        pickle.dump(self.logo_data_in_video, open(logo_data_path, 'wb'))
        logger.i('Logo detection data saved to %s' % logo_data_path)
    
    def _logo_data_with_ads(self):
        ads_to_insert = self.logo_first_occurences
        pos_ads_length = []
        for ad_name in ads_to_insert:
            ad = self.brands_to_detect[ad_name]['ad']
            ad_n_frames = VideoIO(
                ad['video'], 
                self.video_reader.width, 
                self.video_reader.height).get_num_frames()
            pos_ads_length.append((ads_to_insert[ad_name], ad_n_frames))
        pos_ads_length = np.array(sorted(pos_ads_length, key=lambda t: t[0]))
        logger.d('pos_ads_length', pos_ads_length)
        logo_data_with_ads = self.logo_data_in_video.copy()
        logger.d('logo_data_in_video', np.array(self.logo_data_in_video, dtype='object'))
        for t in logo_data_with_ads:
            prev_positions = np.where(pos_ads_length[:, 0] < t[0])[0]
            t[0] += sum(pos_ads_length[prev_positions][:, 1])
        logger.d('logo_data_with_ads', np.array(logo_data_with_ads, dtype='object'))
        return logo_data_with_ads
    
    def generate_video_with_ads(self, video_output, audio_input, audio_output):
        """Generate video with ads inserted at the first occurrences of detected logos
        
        Arguments:
            video_output {str} -- the path of desired video output
            audio_input {str} -- the path of the wav input corresponding to self.video_path
            audio_output {str} -- the path of desired wav output along with the video
        """
        video_input = self.video_path
        width = self.video_reader.width
        height = self.video_reader.height
        ads_to_insert = self.logo_first_occurences
        pos_ads = sorted([(ads_to_insert[k], k)
                              for k in ads_to_insert], key=lambda t: t[0])
        output_video_writer = VideoIO(video_output, width, height, 'w')
        output_audio_writer = AudioIO(audio_input, audio_output, 30)
        start = 0
        for pos, ad_name in pos_ads:
            ad = self.brands_to_detect[ad_name]['ad']
            output_video_writer.copy_frames_from(
                video_input, start, pos - start + 1)
            logger.i('Writing frames [%d:%d]...' % (start, pos))
            output_audio_writer.copy_frames(start, pos - start + 1)
            logger.i('Writing ads [%s]...' % ad_name)
            output_video_writer.copy_frames_from(ad['video'])
            output_audio_writer.copy_frames_from(ad['audio'])
            start = pos + 1
        output_video_writer.copy_frames_from(video_input, start)
        output_audio_writer.copy_frames(start)
        logger.i('Video with new ads saved to (%s, %s)' % (video_output, audio_output))
        logo_data_with_ads = self._logo_data_with_ads()
        logo_data_path = path_util.get_video_logo_data_path(video_output)
        pickle.dump(logo_data_with_ads, open(logo_data_path, 'wb'))
        logger.i('Logo outlines data saved to %s' % logo_data_path)
