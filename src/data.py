import os
os.chdir('..')

DATASETS = [
    {
        'video': 'dataset1/Videos/data_test1.rgb',
        'audio': 'dataset1/Videos/data_test1.wav',
        'width': 480,
        'height': 270,
        'brands_to_detect': ['subway', 'starbucks']
    }, {
        'video': 'dataset2/Videos/data_test2.rgb',
        'audio': 'dataset2/Videos/data_test2.wav',
        'width': 480,
        'height': 270,
        'brands_to_detect': ['mcdonalds', 'nfl']
    }, {
        'video': 'dataset3/Videos/data_test3.rgb',
        'audio': 'dataset3/Videos/data_test3.wav',
        'width': 480,
        'height': 270,
        'brands_to_detect': ['ae', 'hrc']
    }
]

BRANDS = {
    'starbucks': {
        'logo': 'dataset1/Brand Images/starbucks_logo.bmp',
        'ad': {
            'video': 'dataset1/Ads/Starbucks_Ad_15s.rgb',
            'audio': 'dataset1/Ads/Starbucks_Ad_15s.wav'
        }
    },
    'subway': {
        'logo': 'dataset1/Brand Images/subway_logo.bmp',
        'ad': {
            'video': 'dataset1/Ads/Subway_Ad_15s.rgb',
            'audio': 'dataset1/Ads/Subway_Ad_15s.wav'
        }
    },
    'mcdonalds': {
        'logo': 'dataset2/Brand Images/Mcdonalds_logo_2.bmp',
        'ad': {
            'video': 'dataset2/Ads/mcd_Ad_15s.rgb',
            'audio': 'dataset2/Ads/mcd_Ad_15s.wav'
        }
    }, 
    'nfl': {
        'logo': 'dataset2/Brand Images/nfl_logo.bmp',
        'ad': {
            'video': 'dataset2/Ads/nfl_Ad_15s.rgb',
            'audio': 'dataset2/Ads/nfl_Ad_15s.wav'
        }
    },
    'ae': {
        'logo': 'dataset3/Brand Images/ae_logo.bmp',
        'ad': {
            'video': 'dataset3/Ads/ae_ad_15s.rgb',
            'audio': 'dataset3/Ads/ae_ad_15s.wav'
        }
    }, 
    'hrc': {
        'logo': 'dataset3/Brand Images/hrc_logo.bmp',
        'audio': {
            'video': 'dataset3/Ads/hrc_ad_15s.rgb',
            'audio': 'dataset3/Ads/hrc_ad_15s.wav'
        }
    }
}

OUPUTS = [
    {
        'no_ads': {
            'video': 'dataset1/Videos/data_test1_no_ads.rgb',
            'audio': 'dataset1/Videos/data_test1_no_ads.wav'
        }, 
        'new_ads': {
            'video': 'dataset1/Videos/data_test1_new.rgb',
            'audio': 'dataset1/Videos/data_test1_new.wav'
        }
    }, {
        'no_ads': {
            'video': 'dataset2/Videos/data_test2_no_ads.rgb',
            'audio': 'dataset2/Videos/data_test2_no_ads.wav'
        }, 
        'new_ads': {
            'video': 'dataset2/Videos/data_test2_new.rgb',
            'audio': 'dataset2/Videos/data_test2_new.wav'
        }
    }, {
        'no_ads': {
            'video': 'dataset3/Videos/data_test3_no_ads.rgb',
            'audio': 'dataset3/Videos/data_test3_no_ads.wav'
        },
        'new_ads': {
            'video': 'dataset3/Videos/data_test3_new.rgb',
            'audio': 'dataset3/Videos/data_test3_new.wav'
        }
    }
]
