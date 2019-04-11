from src.video_io import VideoIO
import numpy as np
import math

class VideoSegment:

    DIFF_MAX = 30
    DIFF_MIN = 20
    
    def __init__(self, path_video_file, frame_width, frame_height, use_saved=True):
        self.video_io = VideoIO(path_video_file, frame_width, frame_height)
        feature_matrix_path = VideoSegment.get_feature_matrix_path(
            path_video_file)
        if use_saved:
            self.feature_matrix_A = np.load(feature_matrix_path)
        else:
            self.feature_matrix_A = VideoSegment.get_feature_matrix(self.video_io)
            np.save(feature_matrix_path, self.feature_matrix_A)
        self.u, self.s, self.vh = np.linalg.svd(
            self.feature_matrix_A, full_matrices=False)
        print('shape(U) = %s, shape(s) = %s, shape(V.T) = %s' % (
            self.u.shape, self.s.shape, self.vh.shape))

    def _diff_between_frames(self, frame_i, frame_j, kappa=150):
        s, v = self.s, self.vh.T
        sim_square = 0
        for idx in range(kappa):
            sim_square += s[idx] * (v[frame_i, idx] - v[frame_j, idx]) ** 2
        return math.sqrt(sim_square)
    
    def _length_of_psi(self, frame_i):
        rank_A = np.linalg.matrix_rank(self.feature_matrix_A)
        psi_square = 0
        for idx in range(rank_A):
            psi_square += self.vh[frame_i, idx]
        return math.sqrt(psi_square)
    
    def segment(self):
        similarity = [0 for _ in range(self.video_io.get_num_frames())]
        for frame in range(1, len(similarity)):
            similarity[frame] = self._diff_between_frames(frame, frame - 1, kappa=80)
        print(np.where(np.array(similarity) > self.DIFF_MAX))
        import matplotlib.pyplot as plt
        plt.scatter(np.arange(len(similarity)), similarity, s=3)
        plt.show()

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
        print('Total # of frames = %d' % num_frames)
        for i in range(num_frames):
            print('frame #%d' % i)
            frame = video_io.read_frame()
            if frame is None:
                break
            else:
                feature = VideoSegment.create_binned_histograms(frame)
                feature_matrix_A.append(feature)
        feature_matrix_A = np.transpose(feature_matrix_A)
        print('shape(A) =', feature_matrix_A.shape)
        return feature_matrix_A

