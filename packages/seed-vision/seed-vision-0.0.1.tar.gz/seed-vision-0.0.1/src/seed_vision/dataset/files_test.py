from pathlib import Path
from .files import get_image_files


def test_get_image_files():
    images = get_image_files()
    assert isinstance(images, list) is True
    assert len(images) > 0
    assert isinstance(images[0], Path) is True
