from pathlib import Path
from typing import List
import json
from .objects import Object, RectangleObject, SegmentObject
from ..polygons.rectangle import Rectangle
from ..polygons.segment import Segment
from .labels import RECTANGLE_LABELS_DICT, SEGMENT_LABELS_DICT
import numpy as np

class LabelmeAnnotationFile:
    def __init__(self, path:Path) -> None:
        self.path = path

    def load_objects(self, labels, load_segments_as_rectangles=False) -> List[Object]:
        if not self.path.exists():
            return None
        _json = json.load(open(str(self.path), 'r'))
        img_h = _json['imageHeight']
        img_w = _json['imageWidth']
        shapes = _json['shapes']
        objects = []
        for shape in shapes:
            if shape["shape_type"] == 'rectangle':
                points = shape['points']
                x1, y1 = points[0]
                x2, y2 = points[1]
                label_name = shape['label']
                label = RECTANGLE_LABELS_DICT[label_name]

                if label not in labels:
                    continue

                _object = RectangleObject(
                    label=label,
                    position=Rectangle(
                        x1=x1,
                        x2=x2,
                        y1=y1,
                        y2=y2,
                        img_h=img_h,
                        img_w=img_w
                    )
                )
                objects.append(_object)
            elif shape["shape_type"] == 'polygon':
                points = shape['points']
                label_name = shape['label']
                label = SEGMENT_LABELS_DICT[label_name]
                    
                if load_segments_as_rectangles:
                    label = RECTANGLE_LABELS_DICT[label_name]
                    if label not in labels:
                        continue
                    _object = RectangleObject(
                        label=label,
                        position=Rectangle(
                            *Segment.calculate_rectangle(np.array(points)),
                            img_h=img_h,
                            img_w=img_w
                        )
                    )
                elif label in labels:
                    _object = SegmentObject(
                    label=label,
                    position=Segment(
                        points = points,
                        image_h=img_h,
                        image_w=img_w
                    )
                )
                objects.append(_object)
            else:
                continue
        return objects
