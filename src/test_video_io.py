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

dataset_idx = 0
dataset = DATASETS[dataset_idx]
video_io = VideoIO(
    dataset['video'], dataset['width'], dataset['height'])


def get_temp_dir():
    return 'temp/'


def get_frame_image_file_path(path_video_file, frame_idx):
    import os
    dirname = get_temp_dir()
    if not os.path.exists(dirname): 
        os.makedirs(dirname)
    filename = os.path.basename(path_video_file)[:-4]
    filename = '%s_%d.jpg' % (filename, frame_idx)
    return os.path.join(dirname, filename)


def show(f, save=False):
    img = video_io.seek_frame(f)
    img.show()
    if save:
        frame_idx = video_io.get_next_frame_idx() - 1
        img.save(get_frame_image_file_path(video_io.file_path, frame_idx))


def show_this_and_next(f):
    images = [video_io.seek_frame(f), video_io.seek_frame(f + 1)]
    new_im = Image.new('RGB', (dataset['width']*2, dataset['height']))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.show()
