from src.video_segment import VideoSegment

DATASETS = [
    {'video': 'dataset1/Videos/data_test1.rgb', 
    'audio': 'dataset1/Videos/data_test1.wav',
    'width': 480,
    'height': 270},
    {'video': 'dataset2/Videos/data_test2.rgb',
    'audio': 'dataset2/Videos/data_test2.wav',
    'width': 480,
    'height': 270}
    ]

dataset = DATASETS[0]
video_segment = VideoSegment(dataset['video'], dataset['width'], dataset['height'])
video_segment.segment()
