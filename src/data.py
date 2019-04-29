import os
os.chdir('..')

DATASETS = [
    {
        'video': 'dataset1/Videos/data_test1.rgb',
        'audio': 'dataset1/Videos/data_test1.wav',
        'width': 480,
        'height': 270,
        'brand_frames': {
            'subway': 2129,
            'starbucks': 5300
        }
    }, {
        'video': 'dataset2/Videos/data_test2.rgb',
        'audio': 'dataset2/Videos/data_test2.wav',
        'width': 480,
        'height': 270,
        'brand_frames': {
            'mcdonalds': 4400,
            'nfl': -1
        }
    }
]

BRANDS_LOGO = {
    'starbucks': 'dataset1/Brand Images/starbucks_logo.bmp',
    'subway': 'dataset1/Brand Images/subway_logo.bmp',
    'mcdonalds': 'dataset2/Brand Images/Mcdonalds_logo_2.bmp',
    'nfl': 'dataset2/Brand Images/nfl_logo.bmp'
}

EXPECTED_SEGMENTS = [
    {
        'content_shots': [(0, 2399), (2850, 5549), (6000, 8999)],
        'ads_shots': [(2400, 2849), (5550, 5999)]
    }, {
        'content_shots': [(450, 5999), (6500, 9000)],
        'ads_shots': [(0, 449), (6000, 6449)]
    }
]

OUPUTS = [
    'dataset1/Videos/data_test1_no_ads.rgb',
    'dataset2/Videos/data_test2_no_ads.rgb'
]
