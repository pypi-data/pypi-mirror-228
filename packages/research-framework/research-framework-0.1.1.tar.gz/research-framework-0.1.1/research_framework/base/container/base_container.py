import os
from pymongo import MongoClient
from research_framework.base.storage.google_storage import BucketStorage
from dotenv import load_dotenv

load_dotenv()
print("Reading load_dotenv()...")
class BaseContainer:
    client: MongoClient = MongoClient(os.environ["HOST"], tls=False)
    storage: BucketStorage = BucketStorage()
    
    
    @staticmethod
    def register_dao(collection):
        def fun_decorator(fun):
            fun()(BaseContainer.client['framework_test'][collection])
            return fun
        return fun_decorator