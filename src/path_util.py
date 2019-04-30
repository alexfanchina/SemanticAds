import os

def get_video_logo_data_path(path_video_file):
    dirname = os.path.dirname(path_video_file)
    filename = os.path.basename(path_video_file)
    logo_data_filename = '%s.pkl' % filename[:-4]
    return os.path.join(dirname, logo_data_filename)
