from src.video_segment import VideoSegment

FRAME_WIDTH = 480
FRAME_HEIGHT = 270
PATH_VIDEO_FILE = 'dataset2/Videos/data_test2.rgb'
PATH_AUDIO_FILE = 'dataset2/Videos/data_test2.wav'

video_segment = VideoSegment(PATH_VIDEO_FILE, FRAME_WIDTH, FRAME_HEIGHT, use_saved=False)
video_segment.segment()
