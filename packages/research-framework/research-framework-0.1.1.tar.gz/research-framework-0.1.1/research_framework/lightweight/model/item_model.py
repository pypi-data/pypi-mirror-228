from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from bson.objectid import ObjectId
from research_framework.base.model.base_utils import PyObjectId
from research_framework.base.model.base_dao import BaseDao
from research_framework.base.container.base_container import BaseContainer

class ItemTypeModel(BaseModel):
    name: str
    clazz: str


class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    hash_code: str
    clazz: str
    params: Dict[str, Any]
    type: Optional[ItemTypeModel] = None

    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )

@BaseContainer.register_dao('item_collection')
class ItemDao(BaseDao):
    database:Any = None
    
    @classmethod
    def findByHashCode(cls, hash_code):
        if cls.database != None:
            return cls.database.find({'hash_code': hash_code})
        else:
            raise Exception("Dao Not propertly initialized")
        
        
    @classmethod
    def findOneByHashCode(cls, hash_code):
        if cls.database != None:
            return cls.database.find_one({'hash_code': hash_code})
        else:
            raise Exception("Dao Not propertly initialized")
        
    
    @classmethod
    def deleteByHashcode(cls, hash_code, *args, **kwargs) -> Any:
        if cls.database != None:
            return cls.database.delete_one({'hash_code': hash_code}, *args, **kwargs)
        else:
            raise Exception("Dao Not propertly initialized")