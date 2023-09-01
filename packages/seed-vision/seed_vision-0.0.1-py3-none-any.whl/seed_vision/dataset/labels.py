RECTANGLE_LABEL_TYPE = 0
SEGMENT_LABEL_TYPE = 1


class Label:
    def __init__(self, name):
        self.name = name

class RectangleLabel(Label):
    type = RECTANGLE_LABEL_TYPE
    def __init__(self, name):
        super().__init__(name)

class SegmentLabel(Label):
    type = SEGMENT_LABEL_TYPE
    def __init__(self, name):
        super().__init__(name)
    

COFFEE_RECTANGLE_LABEL = RectangleLabel(name='coffee')
BEAN_RECTANGLE_LABEL = RectangleLabel(name='bean')

RECTANGLE_LABELS_LIST = [
    COFFEE_RECTANGLE_LABEL,
    BEAN_RECTANGLE_LABEL
]

SEGMENT_LABELS_LIST =  [
    SegmentLabel(name='coffee'), 
    SegmentLabel(name='bean')
]

LABELS_LIST = RECTANGLE_LABELS_LIST + SEGMENT_LABELS_LIST
RECTANGLE_LABELS_DICT = {l.name:l for l in RECTANGLE_LABELS_LIST}
SEGMENT_LABELS_DICT = {l.name:l for l in SEGMENT_LABELS_LIST}
