import os
from pymongo import MongoClient
from framework.base.storage.google_storage import BucketStorage

class BaseContainer:
    client: MongoClient = MongoClient(os.environ["HOST"], tls=False)
    storage: BucketStorage = BucketStorage()
    
    
    @staticmethod
    def register_dao(collection):
        def fun_decorator(fun):
            fun()(BaseContainer.client['tfm-persistance'][collection])
            return fun
        return fun_decorator