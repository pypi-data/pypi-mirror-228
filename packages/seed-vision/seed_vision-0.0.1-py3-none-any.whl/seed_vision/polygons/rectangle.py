from .position import Position

class Rectangle(Position):
    def __init__(self, x1, y1, x2, y2, img_h, img_w) -> None:
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.x1_rel = x1 / img_w
        self.x2_rel = x2 / img_w
        self.y1_rel = y1 / img_h
        self.y2_rel = y2 / img_h

        self.p1 = (x1, y1)
        self.p2 = (x2, y2)
        self.p1_rel = (self.x1_rel, self.y1_rel)
        self.p2_rel = (self.x2_rel, self.y2_rel)

        self.w = x2 - x1
        self.w_rel = self.w / img_w
        self.h = y2 - y1
        self.h_rel = self.h / img_h

        self.x_c = (x2 + x1) / 2
        self.x_c_rel = self.x_c / img_w
        self.y_c = (y2 + y1) / 2
        self.y_c_rel = self.y_c / img_h

        
