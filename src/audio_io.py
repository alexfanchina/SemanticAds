import wave
import sys

class AudioIO:
    def __init__(self, source_path, output_path, fps):
        self.file_path = source_path
        self.output_path = output_path
        self.fps = fps
        self.audio_file = wave.open(source_path, mode="rb")
        self.output_file = wave.open(self.output_path,mode='wb')
        self.output_file.setnchannels(self.audio_file.getnchannels())
        self.output_file.setsampwidth(self.audio_file.getsampwidth())
        self.output_file.setframerate(self.audio_file.getframerate())

    def write_samples(self, start_index, chunk):
        self.audio_file.setpos(start_index)
        frames_data = self.audio_file.readframes(chunk)
        self.output_file.writeframes(frames_data)

    def copy_frames(self, start_frame=0, num_of_frames=None):
        if num_of_frames is None:
            num_of_frames = self.audio_file.getnframes() - start_frame
        start_index = int(start_frame / self.fps * self.output_file.getframerate())
        chunk = int(num_of_frames / self.fps * self.output_file.getframerate())
        self.write_samples(start_index, chunk)

    def copy_frames_from(self, from_audio_path, start_frame=0, num_of_frames=None):
        from_file = wave.open(from_audio_path, mode="rb")
        if num_of_frames is None:
            num_of_frames = from_file.getnframes() - start_frame
        start_index = int(start_frame / self.fps * self.output_file.getframerate())
        chunk = int(num_of_frames / self.fps * self.output_file.getframerate())
        from_file.setpos(start_index)
        frames_data = self.audio_file.readframes(chunk)
        self.output_file.writeframes(frames_data)

    def close(self):
        self.output_file.close()


if __name__ == "__main__":
    audio_io = AudioIO(sys.argv[1], sys.argv[2], 30)
    audio_io.copy_frames(0, 90)
    # audio_io.copy_frames(90, 90)
    audio_io.copy_frames_from(sys.argv[1], 90, 180)
    audio_io.close()
