import pandas as pd
from pathlib import Path
from . import utils


class Item(object):
    def __repr__(self):
        return f'pastor.item {self.collection}, {self.item}'

    def __init__(self, item, datastore, collection, snapshot=None):
        self.datastore = datastore
        self.collection = collection
        self.snapshot = snapshot
        self.item = item

        self._path = Path(datastore, collection, item)
        if not self._path.exists():
            raise ValueError(
                "Item `%s` doesn't exist. "
                "Create it using collection.write(`%s`, data, ...)" % (
                    item, item))
        if snapshot:
            snap_path = Path(datastore, collection, "_snapshots", snapshot)
            self._path = snap_path.joinpath(item)
            if not snap_path.exists():
                raise ValueError("Snapshot `%s` doesn't exist" % snapshot)
            if not self._path.exists():
                raise ValueError(
                    "Item `%s` doesn't exist in this snapshot" % item)

        self.metadata = utils.read_metadata(self._path)
        self.data = pd.read_feather(self._path)
