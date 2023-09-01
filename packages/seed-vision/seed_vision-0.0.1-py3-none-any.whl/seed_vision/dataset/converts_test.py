from pathlib import Path
from .converters import convert_dataset_to_yolo_format
from .loader import DataLoader
from .labels import RECTANGLE_LABELS_LIST, COFFEE_RECTANGLE_LABEL
from . import EXAMPLE
from ..common.testing import get_tmp_directory

def test_convert():
    dl = DataLoader(images=[
            Path('data/web/4c314570d093e7ac6d46ec70912995a0.jpg'),
            Path('data/web/7b7d733b0a1b09774d65b60c63224b5c.jpg'),
            Path('data/web/76e633e55530c48ce6cebbd152862043.jpg'),
            Path('data/web/18ef26d2d3667003a37aef3754b8c0ad.jpg')
        ], 
        labels=[COFFEE_RECTANGLE_LABEL], 
        load_segments_as_rectangles=True
    )
    convert_dataset_to_yolo_format(
        train=dl,
        val=dl,
        test=dl,
        destination=get_tmp_directory(__file__)
    )
    