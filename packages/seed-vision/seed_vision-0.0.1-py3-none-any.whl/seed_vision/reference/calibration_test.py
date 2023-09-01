from . import LOC
import cv2
from .calibration import find_reference_object

TEST_IMAGE = LOC / 'test_reference.jpeg'


def test_find_reference():
    img = cv2.imread(str(TEST_IMAGE))
    ref_objects = find_reference_object(img)
    assert len(ref_objects) >= 1
    
    

