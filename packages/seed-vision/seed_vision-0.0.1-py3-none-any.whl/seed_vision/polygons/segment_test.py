from seed_vision.common import testing
from seed_vision.dataset.objects import Object
from seed_vision.polygons import Segment
from seed_vision.dataset import EXAMPLE
from seed_vision.dataset.loader import DataLoader
from seed_vision.dataset.labels import SegmentLabel
from seed_vision.presentation.draw import draw_objects
import cv2
from seed_vision.common.testing import get_tmp_directory

        
def test_calculate_seed_size():
    loader = DataLoader([EXAMPLE])
    img, objects = loader[0]
    img = draw_objects(img, objects=objects, draw_object_size_points=True)
    test_directory = get_tmp_directory(__file__)
    cv2.imwrite(str(test_directory / 'seed_size.jpg'), img)


