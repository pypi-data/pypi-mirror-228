from .segment_detector import SegmentDetector
from .clustering import dbscan_segmentation_clustering, gaussian_segmentation_clustering, agglomerative_clustering
import numpy as np
import cv2 as cv

class OpenCVWatershedSegmentDetector(SegmentDetector):
    """
    Source: https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html
    """
    def detect_segments(self, img:np.ndarray):
        #h = int(img.shape[0] / 3)
        #w = int(img.shape[1]/ 3)
        
        #img = cv.resize(img, (w, h), interpolation = cv.INTER_AREA)
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        clusters = agglomerative_clustering(thresh.astype(np.uint8))
        