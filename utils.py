import os
from datetime import datetime
import shutil
import pandas as pd
import numpy as np
from . import config
from pathlib import Path
from orjson import dumps, loads


# def read_csv(urlpath, *args, **kwargs):
#     def rename_dask_index(df, name):
#         df.index.name = name
#         return df
#
#     index_col = index_name = None
#
#     if "index" in kwargs:
#         del kwargs["index"]
#     if "index_col" in kwargs:
#         index_col = kwargs["index_col"]
#         if isinstance(index_col, list):
#             index_col = index_col[0]
#         del kwargs["index_col"]
#     if "index_name" in kwargs:
#         index_name = kwargs["index_name"]
#         del kwargs["index_name"]
#
#     df = dd.read_csv(urlpath, *args, **kwargs)
#
#     if index_col is not None:
#         df = df.set_index(index_col)
#
#     if index_name is not None:
#         df = df.map_partitions(rename_dask_index, index_name)
#
#     return df

#
# def datetime_to_int64(df):
#     """ convert datetime index to epoch int
#     allows for cross language/platform portability
#     """
#
#     if isinstance(df.index, dd.Index) and (
#             isinstance(df.index, pd.DatetimeIndex) and
#             any(df.index.nanosecond) > 0):
#         df.index = df.index.astype(np.int64)  # / 1e9
#
#     return df


def subdirs(d):
    return [o.parts[-1] for o in Path(d).iterdir()]


def read_metadata(path):
    dest = Path(path, 'metadata.oj')
    if path.exists(dest):
        with dest.open() as f:
            return loads(f)


def write_metadata(path, metadata={}):
    now = datetime.now()
    metadata["_updated"] = now.strftime("%Y-%m-%d %H:%I:%S.%f")
    meta_file = Path(path, 'metadata.oj')
    with meta_file.open("w") as f:
        dumps(metadata, f)


def get_path():
    return Path(config.DEFAULT_PATH)


def set_path(path):
    path = get_path() if path is None else path.rstrip("/").rstrip("\\").rstrip(" ")
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


# def set_client(scheduler=None):
#     if scheduler != config._SCHEDULER and config._CLIENT is not None:
#         try:
#             config._CLIENT.shutdown()
#             config._CLIENT = None
#         except Exception:
#             pass
#
#     config._SCHEDULER = scheduler
#     if scheduler is not None:
#         config._CLIENT = Client(scheduler)
#
#     return config._CLIENT
#
#
# def get_client():
#     return config._CLIENT
#
#
# def set_partition_size(size=None):
#     if size is None:
#         size = config.DEFAULT_PARTITION_SIZE * 1
#     config.PARTITION_SIZE = size
#     return config.PARTITION_SIZE
#
#
# def get_partition_size():
#     return config.PARTITION_SIZE