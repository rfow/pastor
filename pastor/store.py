import os
import shutil
from pastor import utils
from pastor.collection import Collection
from pathlib import Path


class store(object):
    def __repr__(self):
        return f'pastor.datastore {self.datastore}'

    def __init__(self, datastore):

        datastore_path = utils.get_path()
        if not datastore_path.exists():
            os.makedirs(datastore_path)

        self.datastore = Path(datastore_path, datastore)
        if not self.datastore.exists():
            os.makedirs(self.datastore)
        self.collections = self.list_collections()

    def _create_collection(self, collection, overwrite=False):
        # create collection (subdir)
        collection_path = Path(self.datastore, collection)
        if collection_path.exists():
            if overwrite:
                self.delete_collection(collection)
            else:
                raise ValueError(
                    "Collection exists! To overwrite, use `overwrite=True`")

        os.makedirs(collection_path)

        # update collections
        self.collections = self.list_collections()

        # return the collection
        return Collection(collection, self.datastore)

    def delete_collection(self, collection):
        # delete collection (subdir)
        shutil.rmtree(Path(self.datastore, collection))

        # update collections
        self.collections = self.list_collections()
        return True

    def list_collections(self):
        # lists collections (subdirs)
        return utils.subdirs(self.datastore)

    def collection(self, collection, overwrite=False):
        if collection in self.collections and not overwrite:
            return Collection(collection, self.datastore)

        # create it
        self._create_collection(collection, overwrite)
        return Collection(collection, self.datastore)
