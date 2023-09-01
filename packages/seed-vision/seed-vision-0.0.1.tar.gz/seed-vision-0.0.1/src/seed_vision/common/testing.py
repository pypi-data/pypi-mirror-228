from pathlib import Path
import shutil
import inspect

def get_tmp_directory(python_file:str):
    called_function = inspect.stack()[1][3]
    path = Path(python_file)
    tmp_dir = path.parent / '.test'/ path.stem / called_function
    if tmp_dir.exists():
        shutil.rmtree(str(tmp_dir))
    tmp_dir.mkdir(parents=True)
    return tmp_dir
