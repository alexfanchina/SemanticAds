import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from logger import logger

class LogoDetector:

    def __init__(self, logo_paths):
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
    
    def detect(self, frame_image):
        _frame = np.array(frame_image)
        frame = cv.cvtColor(_frame, cv.COLOR_RGB2GRAY)
        kp_frame, des_frame = self.sift.detectAndCompute(frame, None)
        for logo in self.logos:
            logo_name, logo_img, kp_logo, des_logo = logo['name'], logo['img'], logo['keypoints'], logo['descriptor']
            logger.d('logo_name', logo_name)
            bf = cv.BFMatcher(cv.NORM_L2, False)
            matches = bf.knnMatch(des_frame, des_logo, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75*n.distance:
                    good.append([m])
            img_match = cv.drawMatchesKnn(frame, kp_frame, logo_img, kp_logo, good, None, flags=2)
            plt.imshow(img_match)
            plt.show()
    
