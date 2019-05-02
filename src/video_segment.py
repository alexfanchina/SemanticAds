from video_io import VideoIO
from audio_io import AudioIO
from logger import logger
import numpy as np
import math
import os

class VideoSegment:
    """Video segmentation module helping to segment and classify content/ad in a video
    """

    FRAME_SIM_MAX = 40
    FRAME_SIM_MIN = 30
    SHOT_SIM_MIN = 0.07
    
    def __init__(self, path_video_file, frame_width, frame_height, use_saved=True):
        """Initialize the video segmentation module with a video
        
        Arguments:
            path_video_file {str} -- path of video to segment
            frame_width {int} -- frame width of the video
            frame_height {int} -- frame height of the video
        
        Keyword Arguments:
            use_saved {bool} -- whether to use saved feature matrix file or not (default: {True})
        """
        self.video_reader = VideoIO(path_video_file, frame_width, frame_height)
        feature_matrix_path = VideoSegment.get_feature_matrix_path(
            path_video_file)
        if use_saved and os.path.exists(feature_matrix_path):
            self.feature_matrix_A = np.load(feature_matrix_path)
        else:
            self.feature_matrix_A = VideoSegment.get_feature_matrix(self.video_reader)
            np.save(feature_matrix_path, self.feature_matrix_A)
        self.u, self.s, self.vh = np.linalg.svd(self.feature_matrix_A, full_matrices=False)
        # print('shape(U) = %s, shape(s) = %s, shape(V.T) = %s' % (
        #     self.u.shape, self.s.shape, self.vh.shape))
        self.shot_boundaries = self._segment()
        logger.d('shot_boundaries', self.shot_boundaries)
        self.content_shots, self.ads_shots = self._tag_content_ads()

    def _difference_between_frames(self, frame_i, frame_j, kappa=150):
        """Calculate the difference between two frames. The higher difference 
        indicates the more visual differences between the two frames.
        
        Arguments:
            frame_i {int} -- index of first frame
            frame_j {int} -- index of second frame
        
        Keyword Arguments:
            kappa {int} -- an parameter controlling the principal components 
            in the feature vectors (default: {150})
        
        Returns:
            float -- difference between two frames
        """
        s, v = self.s, self.vh.T
        diff_square = 0
        for idx in range(kappa):
            diff_square += s[idx] * (v[frame_i, idx] - v[frame_j, idx]) ** 2
        return math.sqrt(diff_square)
    
    def _is_shot_boundary(self, diff, frame_i):
        """Detect if a given frame is the last frame of a shot given all neighbor 
        differences in the video frames
        
        Arguments:
            diff {array} -- all the neighbor differences
            frame_i {int} -- index of the frame to detect
        
        Returns:
            bool -- whether the frame is the last frame of a shot
        """
        assert frame_i < len(diff)
        if frame_i == len(diff) - 1 or diff[frame_i + 1] >= self.FRAME_SIM_MAX:
            return True, frame_i + 1
        elif diff[frame_i + 1] < self.FRAME_SIM_MIN:
            return False, frame_i + 1
        else:
            x = frame_i + 2
            while x + 1 < len(diff) and self._difference_between_frames(frame_i + 1, x) >= self.FRAME_SIM_MIN:
                x += 1
            if self._difference_between_frames(frame_i, x) < self.FRAME_SIM_MAX:
                return True, x + 1
            else:
                return False, frame_i + 1
    
    def _segment(self):
        """Segment the video file into multiple shots
        
        Returns:
            array -- list of shot boundary frame indices
        """
        shot_boundaries = []
        diff = [0 for _ in range(self.video_reader.get_num_frames())]
        for frame in range(1, len(diff)):
            diff[frame] = self._difference_between_frames(frame, frame - 1, kappa=60)
        frame = 0
        while frame < len(diff):
            is_shot_boundary, next = self._is_shot_boundary(diff, frame)
            if is_shot_boundary:
                shot_boundaries.append(frame)
            frame = next
        import matplotlib.pyplot as plt
        plt.scatter(np.arange(len(diff)), diff, s=3)
        plt.show()
        return np.array(shot_boundaries, dtype=int)
    
    def _length_of_psi(self, frame_i):
        v = self.vh.T
        rank_A = np.linalg.matrix_rank(self.feature_matrix_A)
        return np.linalg.norm(v[:rank_A])

    def _length_of_singular_weighted_psi(self, frame_i):
        s, v = self.s, self.vh.T
        rank_A = np.linalg.matrix_rank(self.feature_matrix_A)
        return np.linalg.norm(np.multiply(s[:rank_A], v[:rank_A]))
    
    # def _avg_length_of_psi(self, start_frame, end_frame):
    #     psi_array = [self._length_of_psi(f) 
    #         for f in range(start_frame, end_frame + 1, 2)]
    #     return np.average(psi_array)
    
    # def _avg_length_of_singular_weighted_psi(self, start_frame, end_frame):
    #     sw_psi_array = [self._length_of_singular_weighted_psi(f) 
    #         for f in range(start_frame, end_frame + 1, 2)]
    #     return np.average(sw_psi_array)
    
    def _avg_feature_vector(self, start_frame, end_frame):
        """Get an average feature vector for a series of consecutive frames
        
        Arguments:
            start_frame {int} -- index of the first frame in the frames
            end_frame {int} -- index of the last frame in the frames
        
        Returns:
            array -- average feature vector
        """
        v = self.vh.T
        vectors = v[start_frame: end_frame + 1]
        return np.average(vectors, axis=0)

    def _calc_shots_differences(self):
        """Calculate the differences between every each two shots
        
        Returns:
            array -- the differences between every each two shots
        """
        assert self.shot_boundaries is not None
        shot_first_frame = 0
        shot_vectors = []
        for shot_last_frame in self.shot_boundaries:
            avg_feature_vector = self._avg_feature_vector(shot_first_frame, shot_last_frame)
            shot_vectors.append(avg_feature_vector)
            shot_first_frame = shot_last_frame + 1
        len_shots = len(self.shot_boundaries)
        differences = [[np.linalg.norm(shot_vectors[i] - shot_vectors[j])
             for j in range(len_shots)] for i in range(len_shots)]
        import matplotlib.pyplot as plt
        plt.imshow(differences)
        plt.show()
        return differences

    def _get_shot(self, shot_idx):
        """Get the first and last frame indices in a shot 
        
        Arguments:
            shot_idx {int} -- index of the shot
        
        Returns:
            tupe(int, int) -- the first and last indices in the shot
        """
        assert self.shot_boundaries is not None
        if shot_idx == 0:
            return 0, self.shot_boundaries[shot_idx]
        else:
            return self.shot_boundaries[shot_idx - 1] + 1, self.shot_boundaries[shot_idx]
    
    def _get_shot_duration(self, shot_idx):
        """Get the number of frames in a shot
        
        Arguments:
            shot_idx {int} -- index of the shot
        
        Returns:
            int -- number of frames in the shot
        """
        start, end = self._get_shot(shot_idx)
        return end - start + 1

    def _get_shot_set_duration(self, shot_indices):
        """Get the number of frames in a shot
        
        Arguments:
            shot_indices {array} -- indices of the shots
        
        Returns:
            int -- number of frames in the shots
        """
        shots_duration = [self._get_shot_duration(i) for i in shot_indices]
        return np.sum(shots_duration)

    def _get_longest_shot_idx(self):
        """Get the longest shot in the shots
        
        Returns:
            int -- index of the longest shot
        """
        shot_lengths = [self._get_shot_duration(i) for i in range(len(self.shot_boundaries))]
        return np.argmax(shot_lengths)
    
    def _tag_content_ads(self, threshold=SHOT_SIM_MIN):
        """Tag content/ad to the shots
        
        Keyword Arguments:
            threshold {float} -- a parameter for tagging (default: {SHOT_SIM_MIN})
        
        Returns:
            tupe(list, list) -- indices of content shots and ad shots
        """
        # we assume the longest shot in a video is not ad
        _longest_shot_idx = self._get_longest_shot_idx()
        logger.d('_longest_shot_idx', _longest_shot_idx)
        _similarity = np.array(self._calc_shots_differences()[_longest_shot_idx])
        logger.d('_similarity', _similarity)
        _one_class = np.where(_similarity < threshold)[0]
        _other_class = np.where(_similarity >= threshold)[0]
        if self._get_shot_set_duration(_one_class) > self._get_shot_set_duration(_other_class):
            return _one_class, _other_class
        else:
            return _other_class, _one_class
    
    def get_all_shots(self):
        """Get the first and last frames of all shots
        
        Returns:
            list(tupe(int,int)) -- first and last frames of all shots
        """
        return [self._get_shot(i) for i in range(len(self.shot_boundaries))]

    def get_content_ads_shots(self):
        """Get the first and last frames of content and ad shots
        
        Returns:
            list(tupe(int,int)), list(tupe(int,int)) -- first and last frames of content and ad shots
        """
        content_shots = [self._get_shot(i) for i in self.content_shots]
        ads_shots = [self._get_shot(i) for i in self.ads_shots]
        return np.array(content_shots, dtype='int,int'), np.array(ads_shots, dtype='int,int')
    
    def save_content(self, video_output, audio_input, audio_output):
        """Concatnate the content shots with ads removed and save to a video file
        
        Arguments:
            video_output {str} -- path of the output video file
            audio_input {str} -- path of the corresponding audio file
            audio_output {str} -- path of the output audio file
        """
        logger.i('Saving content shots to %s...' % video_output)
        frame_width = self.video_reader.width
        frame_height = self.video_reader.height
        self.video_writer = VideoIO(video_output, frame_width, frame_height, 'w')
        self.audio_writer = AudioIO(audio_input, audio_output, 30)
        content, _ = self.get_content_ads_shots()
        for content_shot in content:
            start, end = content_shot
            size = end - start + 1
            logger.i('Writing frames [%d:%d]...' % (start, end))
            self.video_reader.seek(start)
            for i in range(size):
                self.video_writer.write_frame(self.video_reader.read_frame())
            self.audio_writer.copy_frames(start, size)
        self.video_writer.close()
        self.audio_writer.close()

    @staticmethod
    def get_feature_matrix_path(path_video_file):
        import os
        dirname = os.path.dirname(path_video_file)
        filename = os.path.basename(path_video_file)
        feature_matrix_filename = '%s_feature.npy' % filename[:-4]
        return os.path.join(dirname, feature_matrix_filename)

    @staticmethod
    def create_binned_histograms(frame, bin=5):
        NUM_CHANNELS = 3
        result = []
        bins = [int(256 / bin * i) for i in range(bin + 1)]
        bins_3d = [bins, bins, bins]
        block_height = int(frame.height / 3)
        block_width = int(frame.width / 3)
        image_arr = np.array(frame)
        for i in range(3):
            for j in range(3):
                block_starting_h = i * block_height
                block_starting_w = j * block_width
                # print("block_starting_h =", block_starting_h)
                # print("block_starting_w =", block_starting_w)
                block = image_arr[
                    block_starting_h: block_starting_h + block_height,
                    block_starting_w: block_starting_w + block_width]
                # print('block =', block)
                hist, _ = np.histogramdd(
                    block.reshape(block_height * block_width, NUM_CHANNELS),
                    bins=bins_3d)
                # print('hist =', hist.astype(int))
                result.extend(hist.astype(int).flatten())
        return result

    @staticmethod
    def get_feature_matrix(video_io):
        feature_matrix_A = []
        num_frames = video_io.get_num_frames()
        logger.d('Total # of frames', num_frames)
        for i in range(num_frames):
            logger.i('Getting feature matrix for frame #%d...' % i)
            frame = video_io.read_frame()
            if frame is None:
                break
            else:
                feature = VideoSegment.create_binned_histograms(frame)
                feature_matrix_A.append(feature)
        feature_matrix_A = np.transpose(feature_matrix_A)
        logger.d('shape(A)', feature_matrix_A.shape)
        return feature_matrix_A
        

