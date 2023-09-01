from os import name
from seed_vision.dataset.labelme import LabelmeAnnotationFile
from pathlib import Path
from typing import List
from .labels import Label, LABELS_LIST
import random
import cv2

class DataLoader:
    def __init__(self, images:List[Path], labels:List[Label]=LABELS_LIST, load_segments_as_rectangles=False) -> None:
        self.length = len(images)
        self.images = images
        self.labels = labels
        self.load_segments_as_rectangles = load_segments_as_rectangles

    def __lenth__(self):
        return self.length
    
    def __getitem__(self, index):
        image_path = self.images[index]
        image, objects = self._load(image_path)
        return image, objects

    def _load(self, path:Path):
        img = cv2.imread(str(path.absolute()))
        annotation_file = self.find_annotation_file(path)
        if annotation_file:
            objects = annotation_file.load_objects(labels=self.labels, load_segments_as_rectangles=self.load_segments_as_rectangles)
        else:
            objects = None
        return img, objects

    def get_labels_names_list(self):
        names = []
        for label in self.labels:
            names.append(label.name)
        return names


    
    @staticmethod
    def find_annotation_file(image_path: Path):
        labelme_path = image_path.with_suffix('.json')
        if labelme_path.exists():
            return LabelmeAnnotationFile(labelme_path)
        return None

    def split(self, chunks, shuffle=True):
        images = self.images.copy()
        if shuffle:
            random.shuffle(images)
        # distrubute images
        chunks_images = []
        for chunk in chunks:
            assert float(chunk) != 0.0
            chunk_volume = int(len(self.images) * chunk)
            chunk_images = images[:chunk_volume]
            images = images[chunk_volume:]
            chunks_images.append(chunk_images)
        if images:
            chunks_images[0] = chunks_images[0] + images
        # return data loaders
        data_loaders = []
        for images in chunks_images:
            data_loaders.append(
                DataLoader(
                    images=images,
                    labels=self.labels,
                    load_segments_as_rectangles=self.load_segments_as_rectangles
                )
            )
        return data_loaders



