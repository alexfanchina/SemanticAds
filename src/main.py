from video_segment import VideoSegment

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
video_segment = VideoSegment(dataset['video'], dataset['width'], dataset['height'])
content, ads = video_segment.get_content_ads_shots()
print('content:\n%s'% content)
print('ads:\n%s' % ads)
