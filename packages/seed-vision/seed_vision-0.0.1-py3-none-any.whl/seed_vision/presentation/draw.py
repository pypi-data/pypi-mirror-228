from ctypes import pointer
from seed_vision.dataset.objects import Object
from seed_vision.polygons import Segment, position
from typing import List
import numpy as np
import cv2
import bbox_visualizer as bbv

A = 0.01
# BGR colors
RED = (0, 0, 255)
GREEN = (0, 200, 0)
BLUE = (200, 0, 0)
BLUE_1 = (150, 0, 0)
BBOX_COLOR = (0, 30, 0)
POLYGON_COLOR = GREEN

def draw_objects(image:np.ndarray,
                objects:List[Object],
                draw_object_size_points=True):
    for object in objects:
        #draw object
        if isinstance(object.position, Segment) and draw_object_size_points:
            size_points_radius = min(image.shape[:2]) * A
            object.position.calculate_seed_size()
            # object sizes
            image = draw_point(image, *object.position.seed_height_p1, radius=size_points_radius)
            image = draw_point(image, *object.position.seed_height_p2, radius=size_points_radius)
            image = draw_point(image, *object.position.seed_width_p1, radius=size_points_radius)
            image = draw_point(image, *object.position.seed_width_p2, radius=size_points_radius)
            image = draw_line(image, object.position.seed_height_p1, object.position.seed_height_p2)
            image = draw_line(image, object.position.seed_width_p1, object.position.seed_width_p2)
            # bbox
            bbox = (int(object.position.x1), int(object.position.y1), int(object.position.x2), int(object.position.y2))
            image = bbv.draw_rectangle(image, bbox, bbox_color=BBOX_COLOR, thickness=1)
            image = bbv.add_label(image, object.label.name, bbox, top=True, draw_bg=False)
            # polygon
            image_original = image.copy()
            contours = object.position.points.astype(int)
            cv2.fillPoly(image, pts = [contours], color=POLYGON_COLOR)
            alpha = 0.4
            image = cv2.addWeighted(image, alpha, image_original, 1 - alpha, 0)
    return image


def draw_point(image, x, y, radius=1):
    try:
        x = int(x)
        y = int(y)
        radius = int(radius)
        image = cv2.circle(image, (x, y), radius=radius, color=BLUE, thickness=-1)
    except:
        pass
    return image
            
def draw_line(image, p1, p2, color=GREEN, thickness=1):
    p1 = (int(p1[0]), int(p1[1]))
    p2 = (int(p2[0]), int(p2[1]))
    image = cv2.line(image, p1, p2, color, thickness)
    return image

