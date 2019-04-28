import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

from src.data import DATASETS as DATASETS
from src.data import BRANDS_LOGO as BRANDS
from src.video_io import VideoIO
from PIL import Image


def show_sift_result(frame, logo):
    sift = cv.xfeatures2d.SIFT_create()
    kp_frame, des_frame = sift.detectAndCompute(frame, None)
    kp_logo, des_logo = sift.detectAndCompute(logo, None)
    bf = cv.BFMatcher(cv.NORM_L2, False)
    matches = bf.knnMatch(des_frame, des_logo, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
    img_match = cv.drawMatchesKnn(
        frame, kp_frame, logo, kp_logo, good, None, flags=2)
    plt.imshow(img_match)
    plt.show()

# def show_orb_result(frame, logo):
#     orb = cv.ORB_create()
#     kp_frame, des_frame = orb.detectAndCompute(frame, None)
#     kp_logo, des_logo = orb.detectAndCompute(logo, None)
#     bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
#     matches = bf.match(des_frame, des_logo)
#     matches = sorted(matches, key=lambda x: x.distance)
#     img3 = cv.drawMatches(frame, kp_frame, logo,
#                         kp_logo, matches[:20], None, flags=2)
#     plt.imshow(img3), plt.show()


# initializing
dataset_idx = 0
logo_name = 'subway'
dataset = DATASETS[dataset_idx]
logo_frame = dataset['brand_frames'][logo_name]
logo_path = BRANDS[logo_name]
video_io = VideoIO(dataset['video'], dataset['width'], dataset['height'])

# getting images for testing
pil_image = video_io.seek_frame(logo_frame).convert('RGB')
_frame = np.array(pil_image)
frame = cv.cvtColor(_frame, cv.COLOR_RGB2GRAY)
_logo = cv.imread(logo_path)
logo = cv.cvtColor(_logo, cv.COLOR_RGB2GRAY)

# show sift
show_sift_result(frame, logo)

## apply yellow-pass mask to frame
# yellowLower = (15, 80, 0)
# yellowUpper = (63, 255, 255)
# blurred = cv.GaussianBlur(_frame, (11, 11), 0)
# hsv = cv.cvtColor(blurred, cv.COLOR_RGB2HSV)
# mask = cv.inRange(hsv, yellowLower, yellowUpper)
# plt.imshow(mask), plt.show()
# frame = mask
# show_sift_result(frame, logo)
