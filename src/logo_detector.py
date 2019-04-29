import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

class LogoDetector:

    def __init__(self, frame_image):
        _frame = np.array(frame_image)
        self.frame = cv.cvtColor(_frame, cv.COLOR_RGB2GRAY)
    
    def detect_sift(self, logo_path):
        _logo = cv.imread(logo_path)
        logo = cv.cvtColor(_logo, cv.COLOR_RGB2GRAY)
        sift = cv.xfeatures2d.SIFT_create(edgeThreshold=10)
        kp_frame, des_frame = sift.detectAndCompute(self.frame, None)
        frame_sift = cv.drawKeypoints(self.frame, kp_frame, None)
        plt.imshow(frame_sift)
        plt.show()
        kp_logo, des_logo = sift.detectAndCompute(logo, None)
        logo_sift = cv.drawKeypoints(logo, kp_logo, None)
        plt.imshow(logo_sift)
        plt.show()
        bf = cv.BFMatcher(cv.NORM_L2, False)
        matches = bf.knnMatch(des_frame, des_logo, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])
        img_match = cv.drawMatchesKnn(self.frame, kp_frame, logo, kp_logo, good, None, flags=2)
        plt.imshow(img_match)
        plt.show()

    # def detect_orb(self, logo_path):
    #     _logo = cv.imread(logo_path)
    #     logo = cv.cvtColor(_logo, cv.COLOR_RGB2GRAY)
    #     orb = cv.ORB_create()
    #     kp_frame, des_frame = orb.detectAndCompute(self.frame, None)
    #     kp_logo, des_logo = orb.detectAndCompute(logo, None)
    #     bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    #     matches = bf.match(des_frame, des_logo)
    #     matches = sorted(matches, key=lambda x: x.distance)
    #     img3 = cv.drawMatches(self.frame, kp_frame, logo, kp_logo, matches[:20], None, flags=2)
    #     plt.imshow(img3), plt.show()

    # def apply_yellow_mask(self, logo):
    #     ## apply yellow-pass mask to frame
    #     yellowLower = (15, 80, 0)
    #     yellowUpper = (63, 255, 255)
    #     blurred = cv.GaussianBlur(self.frame, (11, 11), 0)
    #     hsv = cv.cvtColor(blurred, cv.COLOR_RGB2HSV)
    #     mask = cv.inRange(hsv, yellowLower, yellowUpper)
    #     plt.imshow(mask), plt.show()
    #     frame = mask
    #     self.detect_sift(frame, logo)
