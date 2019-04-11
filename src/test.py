from src.video_io import VideoIO
from PIL import Image

FRAME_WIDTH = 480
FRAME_HEIGHT = 270
PATH_VIDEO_FILE = 'dataset1/Videos/data_test1.rgb'

video_io = VideoIO(PATH_VIDEO_FILE, FRAME_WIDTH, FRAME_HEIGHT)

def show(f):
    video_io.seek_frame(f).show()

def show_this_and_next(f):
    images = [video_io.seek_frame(f), video_io.seek_frame(f + 1)]
    new_im = Image.new('RGB', (FRAME_WIDTH*2, FRAME_HEIGHT))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.show()

show(606)
show_this_and_next(2399)

