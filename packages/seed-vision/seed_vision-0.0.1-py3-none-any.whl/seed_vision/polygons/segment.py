from ctypes import pointer
from .rectangle import Rectangle
from seed_vision.common import algebra as alg
import numpy as np    

class Segment(Rectangle):
    def __init__(self, points:list, image_w=None, image_h=None):
        self.points = np.stack(points)
        self.points_rel = np.multiply(self.points, np.array([1/image_w, 1/image_h]))
        self.seed_size_calculated = False
        self.seed_height = None
        self.seed_width = None
        self.seed_width_p1 = None
        self.seed_width_p2 = None
        self.seed_height_p1 = None
        self.seed_height_p2 = None
        super().__init__(
            *self.calculate_rectangle(self.points), 
            img_w=image_w,
            img_h=image_h 
        )
       
    @staticmethod
    def calculate_rectangle(points: np.ndarray):
        x1 = np.min(points[:, 0])
        y1 = np.min(points[:, 1])
        x2 = np.max(points[:, 0])
        y2 = np.max(points[:, 1])
        return x1, y1, x2, y2
    
    def calculate_seed_size(self):
        if self.seed_size_calculated:
            return
        # s1=[po, p1, ..., pn], s2=s1[p1, p2, ..., pn, p0]
        s1 = self.points
        s2 = np.concatenate([s1[1:],s1[0].reshape(1,2)], axis=0)
        # calculate [a * x + b] of each border
        a = (s2[:,1] - s1[:,1]) / (s2[:,0] - s1[:,0])
        b = s1[:,1] - (a * s1[:,0])
        # central point
        c = np.array([self.x_c, self.y_c])
        # distances of each p points to c
        c_distance_p = np.stack([ alg.points_distance(c, p) for p in self.points])
        # max far p from c
        p1 = self.points[np.argmax(c_distance_p)]
        a_p1, b_p1 = alg.calculate_a_and_b(p1, c)
        # find p2
        def find_most_far_point_in_line(p_rel, a_rel, b_rel):
            p_res = []
            p_res_distance_p_rel = []
            for _p1, _p2, _a, _b,  in zip(s1, s2, a, b):
                if _a == np.inf or _b == np.inf:
                    continue
                _x, _y = alg.calculate_cross(_a, _b, a_rel, b_rel)
                if max(_p1[0], _p2[0]) < _x or min(_p1[0], _p2[0]) > _x or max(_p1[1], _p2[1]) < _y or min(_p1[1], _p2[1]) > _y:
                    continue
                else:
                    p_res.append((_x, _y))
                    p_res_distance_p_rel.append(alg.points_distance(p_rel, (_x, _y)))
            p_res_distance_p_rel = np.array(p_res_distance_p_rel) 
            p_res = p_res[np.argmax(p_res_distance_p_rel)]
            p_res_distance_p_rel = np.max(p_res_distance_p_rel)
            return np.array(p_res), p_res_distance_p_rel

        p2, p2_distance_p1 = find_most_far_point_in_line(p1, a_p1, b_p1)
        # find p3, p4 (width)
        a_w, b_w = alg.calculate_ortogonal_a_and_b(a_p1, c)
        p3, _ = find_most_far_point_in_line(c, a_w, b_w)
        p4, p4_distance_p3 = find_most_far_point_in_line(p3, a_w, b_w)
        # assign seed size
        self.seed_height = p2_distance_p1
        self.seed_width = p4_distance_p3
        self.seed_height_p1 = p1
        self.seed_height_p2 = p2
        self.seed_width_p1 = p3
        self.seed_width_p2 = p4
        self.seed_size_calculated = True