from .loader import DataLoader, Label
from pathlib import Path
from typing import List
import shutil, os

def get_yolo_dataset_config(root, labels:List[Label], train, val, test):
    label_line  = lambda n,label:f'{n}: {label.name}'
    config = '\n'.join(
        [f'path: {root}  # dataset root dir',
        f'train: {train}  # train images',
        f'val: {val}  # val images',
        f'test: {test}  # test images',
        '# Classes',
        'names:\n  ']
    ) +'\n  '.join(label_line(n, label) for n,label in enumerate(labels) )
    return config

def convert_dataset_to_yolo_format(train:DataLoader, val:DataLoader, destination:Path, test:DataLoader=None):

    train_images_path = destination / 'images/train'
    val_images_path = destination / 'images/val'
    test_images_path = destination / 'images/test'
    train_labels_path = destination / 'labels/train'
    val_labels_path = destination / 'labels/val'
    test_labels_path = destination / 'labels/test'

    dataset_config = get_yolo_dataset_config(
        root = str(destination.parent.absolute()),
        labels = train.labels,
        train = train_images_path,
        val = val_images_path,
        test= test_images_path if test else ''
    )

    with open(str(destination / 'yolo.yaml'), 'w') as f:
        f.write(dataset_config)

    def transform_from_data_loader(data_loader:DataLoader, images_path:Path, labels_path:Path):
        labels_name_to_number = {l.name:n for n,l in enumerate(data_loader.labels)}
        if not images_path.exists():
            images_path.mkdir(parents=True)
        if not labels_path.exists():
            labels_path.mkdir(parents=True)
        for (_, objects), image_src_path in zip(data_loader, data_loader.images):
            shutil.copy(str(image_src_path.absolute()), str(images_path.absolute()/image_src_path.name))
            label_path = (labels_path / image_src_path.name).with_suffix('.txt')
            labels_lines = []
            for object in objects:
                labels_lines.append(f'{labels_name_to_number[object.label.name]} {object.transform_to_yolo_label_annotation()}\n')
            with open(label_path, 'w') as f:
                f.writelines(labels_lines)




    transform_from_data_loader(train, train_images_path, train_labels_path)
    transform_from_data_loader(val, val_images_path, val_labels_path)
    if test:
        transform_from_data_loader(test, test_images_path, test_labels_path)



    
    
