import cv2
import numpy as np
from . import LOC
from seed_vision import reference

# img_path, width, height
REFERENCE_OBJECTS = [
    (LOC/'1zl_white.jpeg', 20, 20)
]

def measure_mm_per_pixel(img):
    return

def find_reference_object(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    match_res = []
    for ref_img_path, ref_width_mm, ref_height_mm in REFERENCE_OBJECTS:
        ref_img = cv2.imread(str(ref_img_path))
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
        for ref_img_scaled, scale in get_scaled_reference_image(ref_img):
            _match_res = match_pattern_and_calculate_mm_per_pixel(
                img_gray, 
                ref_img_scaled,
                ref_width_mm,
                ref_height_mm,
                scale=scale
                )
            if _match_res:
                match_res.append(_match_res)
    match_res = sorted(match_res, key=lambda x: x['match_score'], reverse=True)
    return match_res[0]

def get_scaled_reference_image(ref_img, scale_min=0.01, scale_max=4, scale_step=0.05):
    ref_w, ref_h = ref_img.shape[::-1]
    scale_values = np.linspace(scale_min, scale_max, int((scale_max-scale_min)/scale_step))
    for scale in scale_values:
        new_size = (int(ref_w*scale), int(ref_h*scale))
        if new_size[0] < 10 or new_size[1] < 10:
            continue
        yield cv2.resize(ref_img, new_size), scale

def match_pattern_and_calculate_mm_per_pixel(img, ref_img, ref_width_mm, ref_height_mm, scale):
    if img.shape[0]<=ref_img.shape[0] or img.shape[1]<=ref_img.shape[1]:
        return None
    res = cv2.matchTemplate(img, ref_img, cv2.TM_CCOEFF_NORMED)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(res)
    ref_width_pixels, ref_height_pixels = ref_img.shape[::-1]
    mm_per_pixel = np.mean([
        ref_width_mm / ref_width_pixels,
        ref_height_mm / ref_height_pixels
    ])
    return { 'mm_per_pixel': mm_per_pixel, 
             'bbox': (*max_loc, ref_width_pixels, ref_height_pixels), 
             'match_score': max_val,
             'scale':scale
             }