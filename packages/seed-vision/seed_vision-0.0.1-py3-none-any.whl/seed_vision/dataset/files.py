from pathlib import Path

CODE_DATA_DIRNAME = 'data'
CODE_DATA_PATH = Path('.').absolute() / CODE_DATA_DIRNAME
WEB_IMAGES_PATH = CODE_DATA_PATH / 'web'
COFFEE_IMAGES_PATH = CODE_DATA_PATH / 'coffee'

IMAGE_SUFFIXES = ['.jpg','.png']

def get_image_files(path:Path=WEB_IMAGES_PATH):
    images = []
    for img_suffix in IMAGE_SUFFIXES:
        _images = list(path.glob(f'*{img_suffix}'))
        images = images + _images
    return images
