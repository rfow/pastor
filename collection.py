import shutil
from pathlib import Path
from . import utils
from .item import Item
import pandas as pd


class Collection(object):
    def __repr__(self):
        return f'pastor collection : {self.collection}'

    def __init__(self, collection, datastore):
        self.datastore = datastore
        self.collection = collection
        self.items = self.list_items()

    def _item_path(self, item, as_string=False):
        p = Path(self.datastore, self.collection, item)
        if as_string:
            return str(p)
        return p

    def list_items(self, **kwargs):
        dirs = utils.subdirs(Path(self.datastore, self.collection))
        if not kwargs:
            return set(dirs)

        matched = []
        for d in dirs:
            meta = utils.read_metadata(Path(self.datastore, self.collection, d))
            del meta['_updated']

            m = 0
            keys = list(meta.keys())
            for k, v in kwargs.items():
                if k in keys and meta[k] == v:
                    m += 1

            if m == len(kwargs):
                matched.append(d)

        return set(matched)

    def item(self, item, snapshot=None):
        return Item(item, self.datastore, self.collection, snapshot)

    def delete_item(self, item):
        shutil.rmtree(self._item_path(item))
        self.items.remove(item)
        return True

    def write(self, item, data, metadata={}, overwrite=False, **kwargs):

        if self._item_path(item).exists() and not overwrite:
            raise ValueError("""
                Item already exists. To overwrite, use `overwrite=True`.
                Otherwise, use `<collection>.append()`""")

        pd.to_feather(data, self._item_path(item, as_string=True), **kwargs)  # ASSIGN?
        utils.write_metadata(Path(self.datastore, self.collection, item), metadata)
        self.items.add(item)
