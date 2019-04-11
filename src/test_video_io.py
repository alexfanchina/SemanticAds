from src.video_io import VideoIO
from PIL import Image

DATASETS = [
    {
        'video': 'dataset1/Videos/data_test1.rgb',
        'audio': 'dataset1/Videos/data_test1.wav',
        'width': 480,
        'height': 270
    }, {
        'video': 'dataset2/Videos/data_test2.rgb',
        'audio': 'dataset2/Videos/data_test2.wav',
        'width': 480,
        'height': 270
    }
]

dataset_idx = 1
dataset = DATASETS[dataset_idx]
video_io = VideoIO(
    dataset['video'], dataset['width'], dataset['height'])


def show(f):
    video_io.seek_frame(f).show()


def show_this_and_next(f):
    images = [video_io.seek_frame(f), video_io.seek_frame(f + 1)]
    new_im = Image.new('RGB', (dataset['width']*2, dataset['height']))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.show()