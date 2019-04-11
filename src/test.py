from src.video_io import VideoIO

FRAME_WIDTH = 480
FRAME_HEIGHT = 270
PATH_VIDEO_FILE = 'dataset1/Videos/data_test1.rgb'

video_io = VideoIO(PATH_VIDEO_FILE, FRAME_WIDTH, FRAME_HEIGHT)
image = video_io.read_frame()
image.show()
image = video_io.seek_frame(100)
image.show()

