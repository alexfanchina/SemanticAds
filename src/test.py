import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from logger import logger
from video_io import VideoIO
from logo_detector import LogoDetector
from PIL import Image
from data import DATASETS as DATASETS
from data import BRANDS_LOGO as BRANDS

MIN_MATCH_COUNT = 10
MIN_RANSAC_MATCH_COUNT = 5


dataset_idx = 1
logo_name = 'nfl'
dataset = DATASETS[dataset_idx]
logo_frame = dataset['brand_frames'][logo_name]
logo_path = BRANDS[logo_name]

video_io = VideoIO(dataset['video'], dataset['width'], dataset['height'])
pil_image = video_io.read_frame(logo_frame).convert('RGB')
_frame = np.array(pil_image)
frame_img = cv.cvtColor(_frame, cv.COLOR_RGB2GRAY)

_logo_img = cv.imread(logo_path)
logo_img = cv.cvtColor(_logo_img, cv.COLOR_RGB2GRAY)

img1 = logo_img
img2 = frame_img

# do sift
sift = cv.xfeatures2d.SIFT_create(edgeThreshold=10)
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
good = []
for m, n in matches:
    if m.distance < 0.75*n.distance:
        good.append(m)
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32(
        [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32(
        [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    len_mask = np.count_nonzero(matchesMask)
    if len_mask > MIN_RANSAC_MATCH_COUNT:
        logger.d('np.count_nonzero(matchesMask)', len_mask)
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1],
                            [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv.perspectiveTransform(pts, M)
        logger.d('dst', np.int32(dst))
        print( )
        img2 = cv.polylines(img2, [np.int32(dst)], True, 255, 3, cv.LINE_AA)
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)
        img3 = cv.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        plt.imshow(img3, 'gray'), plt.show()
    else:
        logger.i("Not enough matches after ransac: %d/%d" %
                 (len_mask, MIN_RANSAC_MATCH_COUNT))
else:
    logger.i("Not enough matches are found: %d/%d" %
            (len(good), MIN_MATCH_COUNT))
    matchesMask = None

