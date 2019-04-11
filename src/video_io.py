
# rgb channel: each channel 256 = 2^8 => 8 bits = > 1 byte
# pixel: each pixel 3 channels => 3 bytes

import os
from PIL import Image

class VideoIO: 
    def __init__(self, path, width, height, mode='r'):
        self.file_path = path
        self.width = width
        self.height = height
        self.mode = mode
        self.file = open(path, 'rb' if mode == 'r' else 'wb')
        if mode == 'r':
            self.file_size = os.path.getsize(self.file_path)

    def _read_frame_bytes(self):
        frame_length = self.width * self.height * 3
        image_bytes_frame_interleaved = self.file.read(frame_length)
        image_bytes = bytearray(len(image_bytes_frame_interleaved))
        for i in range(len(image_bytes)):
            pixel_index = int(i / 3)
            channel_index = i - pixel_index * 3
            index_in_frame_interleaved = self.width * self.height * channel_index + pixel_index
            image_bytes[i] = image_bytes_frame_interleaved[index_in_frame_interleaved]
        return bytes(image_bytes)

    def read_frame(self):
        if self.file.closed:
            raise EOFError('File is closed.')
        image_bytes = self._read_frame_bytes()
        if (len(image_bytes) > 0):
            return Image.frombytes('RGB', (self.width, self.height), image_bytes)
        else:
            self.file.close()
            return None

    def seek_frame(self, frame_index):
        if self.file.closed:
            self.file = open(self.file_path, 'rb')
        offset = self.width * self.height * 3 * frame_index
        self.file.seek(offset)
        print('File current position =', self.file.tell())
        return self.read_frame()

    def get_num_frames(self):
        assert self.mode == 'r'
        frame_length = self.width * self.height * 3
        return int(self.file_size / frame_length)