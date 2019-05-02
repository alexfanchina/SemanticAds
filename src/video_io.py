
# rgb channel: each channel 256 = 2^8 => 8 bits = > 1 byte
# pixel: each pixel 3 channels => 3 bytes

import os
import numpy as np
from PIL import Image
from logger import logger

class VideoIO: 
    """IO class for easier reading from or writing to given *.rgb video files
    """
    def __init__(self, path, width, height, mode='r'):
        """Initialize VideoIO with video path, video width, video height, and read/write mode
        
        Arguments:
            path {str} -- path of the video to read from or write to
            width {int} -- width of frames in the video
            height {int} -- height of frames in the video
        
        Keyword Arguments:
            mode {{'w', 'r'}} -- read/write mode of the VideoIO (default: {'r'})
        
        Raises:
            ValueError: error for invalid value of mode
        """
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
        """Move the current pointer in the target file to a given frame index position
        
        Arguments:
            frame_index {int} -- the frame index position to set the current pointer
        """
        if self.file.closed:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            self.file = open(
                self.file_path, 'rb' if self.mode == 'r' else 'wb')
        offset = self.width * self.height * 3 * frame_index
        self.file.seek(offset)
        logger.d('file current position', self.file.tell())
    
    def reset(self):
        """Reset everything in the VideoIO class
        """ 
        self.seek(0)

    def _read_frame_bytes(self):
        """Read bytes of a frame and convert it to a numpy byte array representing the RGB image
        
        Returns:
            numpy.array(dtype='b') -- numpy byte array representing the RGB image of the current frame
        """
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
        """Read a frame starting from the next frame or a given frame.
        
        Keyword Arguments:
            frame_index {int} -- the index of a given frame (default: {None})
        
        Raises:
            EOFError: error showing that file is closed
        
        Returns:
            PIL Image -- a PIL image representing the current frame
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
    
    def skip_frame(self, num_of_frames=1):
        """Skip a given number of frames
        
        Keyword Arguments:
            num_of_frames {int} -- the number of frames to skip (default: {1})
        """
        seek_frame = self.get_next_frame_idx() + num_of_frames
        self.seek(seek_frame)

    def get_num_frames(self):
        """Get the total number of frames in the current video file
        
        Returns:
            int -- the total number of frames in the current video file
        """
        assert self.mode == 'r'
        frame_length = self.width * self.height * 3
        return int(self.file_size / frame_length)

    def write_frame(self, image):
        """Write a frame image to the current pointer position of the video file
        
        Arguments:
            image {PIL Image} -- the image to write as a frame
        
        Raises:
            EOFError: error showing that file is closed
        """
        assert self.mode == 'w'
        if self.file.closed:
            raise EOFError('File is closed.')
        frame_size = self.width * self.height
        frame_length = frame_size * 3
        image_bytes = np.array(bytearray(image.tobytes()), dtype='b')
        image_interleaved = np.zeros(frame_length, dtype='b')
        image_interleaved[0:frame_size] = image_bytes[0::3]
        image_interleaved[frame_size:frame_size*2] = image_bytes[1::3]
        image_interleaved[frame_size*2:frame_size*3] = image_bytes[2::3]
        self.file.write(bytes(image_interleaved))
    
    def copy_frames_from(self, input_path, start_frame=0, num_of_frames=None):
        """Copy frames from another input video file
        
        Arguments:
            input_path {str} -- the path of the video file to copy from
        
        Keyword Arguments:
            start_frame {int} -- the starting frame in `input_path` to copy (default: {0})
            num_of_frames {int} -- the number of frames in `input_path` to copy (default: {None})
        """
        reader = VideoIO(input_path, self.width, self.height, 'r')
        reader.seek(start_frame)
        end_frame = reader.get_num_frames() if num_of_frames is None else min(
            reader.get_num_frames(), start_frame + num_of_frames)
        while reader.get_next_frame_idx() < end_frame:
            image = reader.read_frame()
            self.write_frame(image)
        reader.close()

    def get_next_frame_idx(self):
        """Get the index of next reading/writing frame
        
        Returns:
            int -- the index of next reading/writing frame in the current video file
        """
        frame_length = self.width * self.height * 3
        return int(self.file.tell() / frame_length)
    
    def close(self):
        """Close the current file. This should be called after reading/writing all the data
        """
        self.file.close()
