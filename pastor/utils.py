import os
import shutil
from pastor import config
from pathlib import Path
from orjson import dumps, loads


def subdirs(d):
    return [o.parts[-1] for o in Path(d).iterdir()]


def read_metadata(path):
    if path.exists():
        with path.open() as f:
            return loads(f.read())


def write_metadata(path, metadata):
    meta_file = Path(path, 'metadata.oj')
    metadata = dumps(metadata)
    with meta_file.open("wb") as f:
        f.write(metadata)


def get_path():
    return Path(config.DEFAULT_PATH)


def set_path(path):
    path = get_path() if path is None else Path(path)
    config.DEFAULT_PATH = path
    if not path.exists():
        os.makedirs(path)
    return path


def list_stores():
    path = get_path()
    if not path.exists():
        os.makedirs(path)
    return subdirs(path)


def delete_store(store):
    shutil.rmtree(get_path().joinpath(store))
    return True


def delete_stores():
    shutil.rmtree(get_path())
    return True
