from .loader import DataLoader
from . import EXAMPLE

def test_data_loader_init():
    loader = DataLoader([EXAMPLE])
    assert isinstance(loader, DataLoader) is True

def test_data_loader_getitem():
    loader = DataLoader([EXAMPLE])
    assert loader[0] is not None


