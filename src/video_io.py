
# rgb channel: each channel 256 = 2^8 => 8 bits = > 1 byte
# pixel: each pixel 3 channels => 3 bytes

import os
import numpy as np
from PIL import Image

class VideoIO: 
    def __init__(self, path, width, height, mode='r'):
        self.file_path = path
        self.width = width
        self.height = height
        if mode not in ['r', 'w']:
            raise ValueError('Param mode must be \'r\' or \'w\'.')
        self.mode = mode
        self.file = open(path, 'rb' if mode == 'r' else 'wb')
        if mode == 'r':
            self.file_size = os.path.getsize(self.file_path)

    def seek(self, frame_index):
        if self.file.closed:
            self.file = open(
                self.file_path, 'rb' if self.mode == 'r' else 'wb')
        offset = self.width * self.height * 3 * frame_index
        self.file.seek(offset)
        print('File current position =', self.file.tell())

    def _read_frame_bytes(self):
        frame_size = self.width * self.height
        frame_length = frame_size * 3
        image_interleaved_bytes = self.file.read(frame_length)
        image_interleaved = np.array(bytearray(image_interleaved_bytes), dtype='b')
        image = np.zeros(frame_length, dtype='b')
        image[0::3] = image_interleaved[0:frame_size]
        image[1::3] = image_interleaved[frame_size:frame_size*2]
        image[2::3] = image_interleaved[frame_size*2:frame_size*3]
        return image

    def read_frame(self, frame_index=None):
        """
        Read frame. If `frame_index` is None, read the next frame, else read the 
        `frame_index`-th frame.
        """
        if self.file.closed:
            raise EOFError('File is closed.')
        if frame_index is not None:
            self.seek(frame_index)
        image_bytes = self._read_frame_bytes()
        if (len(image_bytes) > 0):
            return Image.frombytes('RGB', (self.width, self.height), image_bytes)
        else:
            self.file.close()
            return None

    def get_num_frames(self):
        assert self.mode == 'r'
        frame_length = self.width * self.height * 3
        return int(self.file_size / frame_length)

    def write_frame(self, image):
        assert self.mode == 'w'
        if self.file.closed:
            raise EOFError('File is closed.')
        frame_size = self.width * self.height
        frame_length = frame_size * 3
        image_bytes = image.tobytes()
        image_interleaved = np.zeros(frame_length, dtype='b')
        image_interleaved[0:frame_size] = image_bytes[0::3]
        image_interleaved[frame_size:frame_size*2] = image_bytes[1::3]
        image_interleaved[frame_size*2:frame_size*3] = image_bytes[2::3]

    def get_next_frame_idx(self):
        frame_length = self.width * self.height * 3
        return self.file.tell() / frame_length
    
    def close(self):
        self.file.close()
