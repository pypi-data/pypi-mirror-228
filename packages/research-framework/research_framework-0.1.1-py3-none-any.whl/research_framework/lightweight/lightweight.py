import logging
from typing import Any
from research_framework.lightweight.model.item_model import ItemDao, ItemModel
from research_framework.base.container.base_container import BaseContainer

class FlyWeight:
    
    def get_item(self, hash_code):
        response = ItemDao.findByHashCode(hash_code)
        if response != None:
            doc = ItemModel(**response)
        return None
    
    def set_item(self, item:ItemModel, data:Any):
        with BaseContainer.client.start_session() as session:
            with session.start_transaction():
                try:
                    
                    result = ItemDao.create(item, session=session)
                    if result.inserted_id != None:
                        BaseContainer.storage.upload_file(file=data, file_name=item.hash_code)
                        session.commit_transaction()
                        return True
                    else:
                        print("Item already exists")
                        return False
                except Exception as ex:
                    try:
                        session.abort_transaction()
                        BaseContainer.storage.delete_file(item.hash_code)
                    except Exception as ex2:
                        print(ex2)
                        return False
                    print(ex)
                    return False
                
    def unset_item(self, item:ItemModel):
        with BaseContainer.client.start_session() as session:
            with session.start_transaction():
                try:
                    result = ItemDao.deleteByHashcode(item.hash_code, session=session)
                    if result.deleted_count == 1:
                        BaseContainer.storage.delete_file(item.hash_code)
                        session.commit_transaction()
                        return True
                    else:
                        print("Item already exists")
                        return False
                except Exception as ex:
                    try:
                        session.abort_transaction()
                    except Exception as ex2:
                        print(ex2)
                        return False
                    print(ex)
                    return False
                    
    def forward(self, item, data):
        if len(list(ItemDao.findByHashCode(item.hash_code))) == 0:
            print("Item not found")
            if not self.set_item(item, data):
                raise Exception("Error saving item")
        else:
            print("Item already exists")
        
        return item, data 
    
    
        
                        
                    
    
            
            
        