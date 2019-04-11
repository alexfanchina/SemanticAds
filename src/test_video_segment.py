from video_segment import VideoSegment
import numpy as np

def in_shots(s, shots):
    if type(shots) is tuple:
        return s[0] >= shots[0] and s[1] <= shots[1]
    else:
        result = False
        for shot in shots:
            result = result or in_shots(s, shot)
        return result

def get_expected_indices(segment_shots, expected_contents):
    content_indices = []
    ads_indices = []
    for i, shot in enumerate(segment_shots):
        if in_shots(shot, expected_contents):
            content_indices.append(i)
        else:
            ads_indices.append(i)
    return np.array(content_indices), np.array(ads_indices)


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

EXPECTED = [
    {
        'content_shots': [(0, 2399), (2850, 5549), (6000, 8999)],
        'ads_shots': [(2400, 2849), (5550, 5999)]
    }, {
        'content_shots': [(450, 5999), (6500, 9000)],
        'ads_shots': [(0, 449), (6000, 6449)]
    }
]

dataset_idx = 1
dataset = DATASETS[dataset_idx]
video_segment = VideoSegment(
    dataset['video'], dataset['width'], dataset['height'])
content, ads = video_segment.get_content_ads_shots()

print()
content_expected, ads_expected = get_expected_indices(
    video_segment.get_all_shots(), EXPECTED[dataset_idx]['content_shots'])
print('shots:\n%s' % np.array(video_segment.get_all_shots()))
print('content:\n%s' % video_segment.content_shots)
print('content_expected:\n%s' % content_expected)
print('ads:\n%s' % video_segment.ads_shots)
print('ads_expected:\n%s' % ads_expected)
