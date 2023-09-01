from ..dataset.loader import DataLoader
from ..dataset import EXAMPLE
from .opencv import OpenCVWatershedSegmentDetector

"""def test_opencv_watershed_segment_detector():
    dl = DataLoader(images=[EXAMPLE])
    detector = OpenCVWatershedSegmentDetector()
    img, objects = dl[0]
    res = detector.detect_segments(img)
    assert res is not None

"""