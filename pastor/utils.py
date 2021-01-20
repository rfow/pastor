import os
import shutil
from pathlib import Path
from orjson import dumps, loads
from pastor import store


def connect(store_path, store_name, collection):
    s = store(store_path, store_name)
    return s.collection(collection)


def subdirs(d):
    return [o.parts[-1] for o in Path(d).iterdir()]


def read_metadata(path):
    with path.open() as f:
        return loads(f.read())


def write_metadata(path, metadata):
    meta_file = Path(path, 'metadata.oj')
    metadata = dumps(metadata)
    with meta_file.open("wb") as f:
        f.write(metadata)


def list_stores(path):
    if not path.exists():
        os.makedirs(path)
    return subdirs(path)


def delete_store(path, store):
    shutil.rmtree(Path(path).joinpath(store))
    return True


def delete_stores(path):
    shutil.rmtree(Path(path))
    return True


def dict_search(dictionary, **kwargs):
    for k, v in kwargs.items():
        if k not in dictionary.keys() or not dictionary[k] == v:
            return False
    return True
