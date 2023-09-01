from .labels import Label
from ..polygons.position import Position
from ..polygons.rectangle import Rectangle

OBJECT_RECTANGLE_TYPE = 0
OBJECT_SEGMENT_TYPE = 1

class Object:
    def __init__(self, label:Label, position:Position) -> None:
        self.label = label
        self.position = position
    

class RectangleObject(Object):
    def transform_to_yolo_label_annotation(self):
        return f'{self.position.x_c_rel:.6f} {self.position.y_c_rel:.6f} {self.position.w_rel:.6f} {self.position.h_rel:.6f}'



class SegmentObject(Object):
    def transform_to_yolo_label_annotation(self):
        points = ' '.join(f'{p[0]:.6f} {p[1]:.6f}' for p in self.position.points_rel)
        #return f'{self.position.x1_rel:.6f} {self.position.y1_rel:.6f} {self.position.x2_rel:.6f} {self.position.y2_rel} {points}'
        return f'{points}'



