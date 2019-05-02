import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from logger import logger
import util

class LogoDetector:
    """Logo detector class that contains logos information and helps to detect logos in a single frame
    """

    MIN_MATCH_COUNT = 10
    MIN_RANSAC_MATCH_COUNT = 5

    def __init__(self, logo_paths):
        """Initialize LogoDetector with paths of logos
        
        Arguments:
            logo_paths {dict} -- dict of logo paths in {<logo_name>: <logo_path>} format
        """
        self.logos = []
        self.sift = cv.xfeatures2d.SIFT_create(edgeThreshold=10)
        for logo_name in logo_paths:
            logo_path = logo_paths[logo_name]
            _logo_img = cv.imread(logo_path)
            logo_img = cv.cvtColor(_logo_img, cv.COLOR_RGB2GRAY)
            kp_logo, des_logo = self.sift.detectAndCompute(logo_img, None)
            logo = {
                'name': logo_name, 
                'img': logo_img, 
                'keypoints': kp_logo, 
                'descriptor': des_logo}
            self.logos.append(logo)
    
    def _sift_match(self, logo, frame_img):
        """Use SIFT to match a logo to a given frame image
        
        Arguments:
            logo {dict} -- dict of logo with name, image, key points, and descriptor
            frame_img {cv Image} -- an OpenCV image
        
        Returns:
            numpy.ndarray or None -- a polygone representing homography if there are valid matches else None
        """
        logo_name, logo_img = logo['name'], logo['img']
        kp_logo, des_logo = logo['keypoints'], logo['descriptor']
        logger.d('logo_name', logo_name)
        kp_frame, des_frame = self.sift.detectAndCompute(frame_img, None)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des_logo, des_frame, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.75*n.distance:
                good.append(m)
        if len(good) > LogoDetector.MIN_MATCH_COUNT:
            src_pts = np.float32(
                [kp_logo[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32(
                [kp_frame[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 1.0)
            matchesMask = mask.ravel().tolist()
            len_mask = np.count_nonzero(matchesMask)
            if len_mask > LogoDetector.MIN_RANSAC_MATCH_COUNT:
                logger.d('np.count_nonzero(matchesMask)', len_mask)
                h, w = logo_img.shape
                pts = np.float32([[0, 0], [0, h-1], [w-1, h-1],
                                [w-1, 0]]).reshape(-1, 1, 2)
                dst = cv.perspectiveTransform(pts, M)
                logger.d('dst', dst)
                poly = np.int32(dst).reshape(4, 2)
                if util.valid_poly(poly):
                    # frame_img = cv.polylines(frame_img, [np.int32(dst)], True, 255, 3, cv.LINE_AA)
                    # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                    #                 singlePointColor=None,
                    #                 matchesMask=matchesMask,  # draw only inliers
                    #                 flags=2)
                    # img3 = cv.drawMatches(
                    #     logo_img, kp_logo, frame_img, kp_frame, good, None, **draw_params)
                    # plt.imshow(img3, 'gray'), plt.show()
                    return poly
                else:
                    logger.d("Polygon not valid")
            else:
                logger.d("Not enough matches after ransac: %d/%d" %
                         (len_mask, LogoDetector.MIN_RANSAC_MATCH_COUNT))
        else:
            logger.d("Not enough matches are found: %d/%d" %
                     (len(good), LogoDetector.MIN_MATCH_COUNT))
            matchesMask = None
        return None
    
    def detect(self, frame_image):
        """Detect a given frame image with each logo in the detector
        
        Arguments:
            frame_image {PIL Image} -- an image to detect logos
        
        Returns:
            dict -- dict in {<logo_name>: <polygon>} representing detected logo areas
        """
        _frame = np.array(frame_image)
        frame = cv.cvtColor(_frame, cv.COLOR_RGB2GRAY)
        brand_areas = []
        for logo in self.logos:
            poly = self._sift_match(logo, frame)
            if poly is not None:
                brand_areas.append((logo['name'], poly))
        return brand_areas

    
