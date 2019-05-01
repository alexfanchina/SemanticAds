import os
from video_io import VideoIO
from data import DATASETS as DATASETS
from PIL import Image

dataset_idx = 0
dataset = DATASETS[dataset_idx]
video_io = VideoIO(
    dataset['video'], dataset['width'], dataset['height'])

def get_temp_dir():
    return 'temp/'

def get_frame_image_file_path(path_video_file, frame_idx):
    dirname = get_temp_dir()
    if not os.path.exists(dirname): 
        os.makedirs(dirname)
    filename = os.path.basename(path_video_file)[:-4]
    filename = '%s_%d.jpg' % (filename, frame_idx)
    return os.path.join(dirname, filename)

def get_output_video_path(filename):
    return (get_temp_dir(), '%s.rgb' % filename)

def show(f, save=False):
    img = video_io.read_frame(f)
    img.show()
    if save:
        frame_idx = video_io.get_next_frame_idx() - 1
        img.save(get_frame_image_file_path(video_io.file_path, frame_idx))

def show_this_and_next(f):
    images = [video_io.read_frame(f), video_io.read_frame(f + 1)]
    new_im = Image.new('RGB', (dataset['width']*2, dataset['height']))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.show()


if __name__ == "__main__":
    show(4012)