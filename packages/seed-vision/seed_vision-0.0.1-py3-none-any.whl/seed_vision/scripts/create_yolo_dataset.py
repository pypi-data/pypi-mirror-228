from pathlib import Path
from ..dataset.files import WEB_IMAGES_PATH, COFFEE_IMAGES_PATH
from ..dataset.converters import convert_dataset_to_yolo_format
from ..dataset.loader import DataLoader
from ..dataset.labels import RECTANGLE_LABELS_LIST, COFFEE_RECTANGLE_LABEL, SEGMENT_LABELS_LIST
from ..common.testing import get_tmp_directory
from ..dataset.files import get_image_files
from ..common.files import ensure_empty_directory

def create_yolo_rectangle_dataset(destination:Path):
    destination = ensure_empty_directory(destination)
    data_loader = DataLoader(
        images=get_image_files(WEB_IMAGES_PATH) + get_image_files(COFFEE_IMAGES_PATH), 
        labels=RECTANGLE_LABELS_LIST, 
        load_segments_as_rectangles=True
    )
    train_dl, val_dl = data_loader.split([0.8,0.2])
    test_dl = val_dl
    convert_dataset_to_yolo_format(
        train=train_dl,
        val=val_dl,
        test=test_dl,
        destination=destination
    )

def create_yolo_segment_dataset(destination:Path):
    destination = ensure_empty_directory(destination)
    data_loader = DataLoader(
        images=get_image_files(WEB_IMAGES_PATH) + get_image_files(COFFEE_IMAGES_PATH), 
        labels=SEGMENT_LABELS_LIST
    )
    train_dl, val_dl = data_loader.split([0.8,0.2])
    test_dl = val_dl
    convert_dataset_to_yolo_format(
        train=train_dl,
        val=val_dl,
        test=test_dl,
        destination=destination
    )
    