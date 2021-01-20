import shutil
from pathlib import Path
from pastor import utils
import os
import pandas as pd
import feather


class Collection(object):
    def __repr__(self):
        return f'pastor collection : {self.collection}'

    def __init__(self, collection, datastore):
        self.datastore = datastore
        self.collection = collection

    def _item_path(self, item, as_string=False):
        p = Path(self.datastore, self.collection, item)
        if as_string:
            return str(p)
        return p

    def list_items(self, **kwargs):
        dirs = utils.subdirs(Path(self.datastore, self.collection))
        if not kwargs:
            return dirs

        meta_paths = [Path(self.datastore, self.collection, d, 'metadata.oj') for d in dirs]
        meta_dicts = [utils.read_metadata(meta_path) for meta_path in meta_paths if meta_path.exists()]
        matches = [meta_dict['id'] for meta_dict in meta_dicts if utils.dict_search(meta_dict, **kwargs)]
        return matches

    def delete_item(self, item):
        shutil.rmtree(self._item_path(item))
        return True

    def write_item(self, item, data, metadata=None, overwrite=False):
        if self._item_path(item).exists() and not overwrite:
            raise ValueError('Item already exists. To overwrite, use overwrite=True.')
        elif not self._item_path(item).exists():
            os.makedirs(self._item_path(item))
        data.index.rename('date', inplace=True)
        data.reset_index(inplace=True)
        if metadata:
            utils.write_metadata(Path(self.datastore, self.collection, item), metadata)
        data.to_feather(Path(self.datastore, self.collection, item, f'{item}.ftr'))

    def upsert_item(self, item, new_data, metadata=None):
        if not self._item_path(item).exists():
            self.write_item(item, new_data, metadata)
        else:
            data = self.read_item(item)
            old_meta = data._metadata
            try:
                data.update(new_data)
            except Exception as e:
                raise ValueError(f'Upsert issue for {item}.\n'
                                 f'New df: {new_data}\n'
                                 f'Old df: {data}\n'
                                 f'Exception: {str(e)}')
            else:
                new_meta = metadata if metadata is not None else old_meta
                self.write_item(item, data, new_meta, overwrite=True)

    def read_item(self, item):
        if not self._item_path(item).exists():
            raise ValueError(f'{item} folder not present in {self.collection}')
        data = pd.read_feather(Path(self._item_path(item), f'{item}.ftr'))
        data.set_index(data.columns[0], inplace=True)

        meta_path = Path(self._item_path(item), 'metadata.oj')
        if meta_path.exists():
            metadata = utils.read_metadata(meta_path)
            data._metadata = metadata
        return data
