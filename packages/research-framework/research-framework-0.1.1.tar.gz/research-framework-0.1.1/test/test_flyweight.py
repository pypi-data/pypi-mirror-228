import pytest
from typing import Any, Tuple
from research_framework.base.container.base_container import BaseContainer
from research_framework.lightweight.model.item_model import ItemModel, ItemDao
from research_framework.lightweight.lightweight import FlyWeight

@pytest.fixture
def test_save_new_item():
    fly = FlyWeight()
    
    item = ItemModel(
        name='test',
        hash_code='TestHashCode_123321',
        clazz='ClazzToItemModel',
        params={
            'param1': 1,
            'param2': 2,
        }
    )
    
    obj = {'name': 'test', 'message': 'Esto es un objeto test'}
    
    print("HERE")
    fly.forward(item, obj)
    print("Forwarded")
    assert True == BaseContainer.storage.check_if_exists(item.hash_code)
    assert obj == BaseContainer.storage.download_file(item.hash_code)
    stored = ItemModel(**ItemDao.findOneByHashCode(item.hash_code))
    stored.id = None
    item.id = None
    assert item.model_dump() == stored.model_dump()
    
    return item, obj, fly


@pytest.fixture
def save_new_item_delete_at_the_end(test_save_new_item:Tuple[ItemModel, Any, FlyWeight], request):
    item, _, fly = test_save_new_item
    request.addfinalizer(lambda: fly.unset_item(item))
    return test_save_new_item


def test_save_existing_item(save_new_item_delete_at_the_end: Tuple[ItemModel, Any, FlyWeight]):
    item, obj, fly = save_new_item_delete_at_the_end
    
    item = ItemModel(
        name='test',
        hash_code='TestHashCode_123321',
        clazz='ClazzToItemModel',
        params={
            'param1': 1,
            'param2': 2,
        }
    )
    
    obj = {'name': 'test', 'message': 'Esto es un objeto test'}
    
    fly.forward(item, obj)
    
    assert 1 == len(list(ItemDao.findByHashCode(item.hash_code)))
    
def test_delete_existing_item(test_save_new_item: Tuple[ItemModel, Any, FlyWeight]):
    item, _, fly = test_save_new_item
    
    fly.unset_item(item)
    
    assert ItemDao.findOneByHashCode(item.hash_code) == None
    assert BaseContainer.storage.check_if_exists(item.hash_code) == False
    
    
    
    

    
    
    