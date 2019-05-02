import wave
import sys

class AudioIO:
    """IO class for easier writing or copying data to audio file
    """
    def __init__(self, source_path, output_path, fps):
        """Initialize AudioIO with source path, output path, and fps. 
        
        Arguments:
            source_path {str} -- path of source file used to initialize the output file
            output_path {str} -- path of output file to write
            fps {int} -- the frame rate of the video corresponding to the output file
        """
        self.source_path = source_path
        self.output_path = output_path
        self.fps = fps
        self.source_file = wave.open(source_path, mode="rb")
        self.output_file = wave.open(self.output_path,mode='wb')
        self.output_file.setnchannels(self.source_file.getnchannels())
        self.output_file.setsampwidth(self.source_file.getsampwidth())
        self.output_file.setframerate(self.source_file.getframerate())

    def write_samples(self, start_index, chunk):
        """Copy samples from the current source in samples
        
        Arguments:
            start_index {int} -- the start position to copy in the number of audio samples
            chunk {int} -- the length of audio to copy in the number of audio samples
        """
        self.source_file.setpos(start_index)
        frames_data = self.source_file.readframes(chunk)
        self.output_file.writeframes(frames_data)

    def copy_frames(self, start_frame=0, num_of_frames=None):
        """Copy frames from the current source in video frames
        
        Keyword Arguments:
            start_frame {int} -- the start position to copy in the number of video frames (default: {0})
            num_of_frames {int} -- the length of audio to copy in the number of video frames (default: {None})
        """
        if num_of_frames is None:
            num_of_frames = self.source_file.getnframes() - start_frame
        start_index = int(start_frame / self.fps * self.output_file.getframerate())
        chunk = int(num_of_frames / self.fps * self.output_file.getframerate())
        self.write_samples(start_index, chunk)

    def copy_frames_from(self, from_audio_path, start_frame=0, num_of_frames=None):
        """Copy frames from a specific path
        
        Arguments:
            from_audio_path {str} -- the path of audio file to copy from
        
        Keyword Arguments:
            start_frame {int} -- the start position to copy in the number of video frames (default: {0})
            num_of_frames {int, None} -- the length of audio to copy in the number of video frames (default: {None})
        """
        from_file = wave.open(from_audio_path, mode="rb")
        if num_of_frames is None:
            num_of_frames = from_file.getnframes() - start_frame
        start_index = int(start_frame / self.fps * self.output_file.getframerate())
        chunk = int(num_of_frames / self.fps * self.output_file.getframerate())
        from_file.setpos(start_index)
        frames_data = from_file.readframes(chunk)
        self.output_file.writeframes(frames_data)

    def close(self):
        """Close the current files. This should be called after writing all the data
        """
        self.source_file.close()
        self.output_file.close()


if __name__ == "__main__":
    source = '../dataset1/Videos/data_test1.wav'
    dest = '../temp/test.wav'
    ad = '../dataset1/Ads/Subway_Ad_15s.wav'
    audio_io = AudioIO(source, dest, 30)
    audio_io.copy_frames(0, 90)
    audio_io.copy_frames_from(ad)
    audio_io.copy_frames(90, 90)
    audio_io.close()
