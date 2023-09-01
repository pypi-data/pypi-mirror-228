import shutil
from pathlib import Path

def ensure_empty_directory(directory:Path):
    if type(directory) is not Path:
        directory = Path(directory)
    if directory.exists():
        shutil.rmtree(str(directory))
    directory.mkdir(parents=True)
    return directory