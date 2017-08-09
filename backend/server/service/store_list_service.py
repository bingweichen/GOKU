"""

@author: Bingwei Chen

@time: 2017.08.08

@desc: service for store_list

1. store_list Add/Get/Modify/Remove

2. 电动车销售库存 更改 Add/Get/Modify/Remove

"""
from playhouse.shortcuts import model_to_dict

from server.database.model import StoreList
from server.utility.json_utility import models_to_json


def add(**kwargs):
    """
    add store_list

    eg = {
    "model": "E100小龟",
    "color": "红",
    "num": 50

    }

    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    store_list = StoreList.create(**kwargs)
    return model_to_dict(store_list)


def get(*query, **kwargs):
    store_list = StoreList.get(*query, **kwargs)
    return model_to_dict(store_list)


def get_all():
    store_lists = StoreList.select()
    return models_to_json(store_lists)


def get_by_id(store_list_id):
    return model_to_dict(StoreList.get(StoreList.id == store_list_id))


def get_by_model_color(model, color):
    store_lists = StoreList.select().where(
        StoreList.model == model, color == color)
    return models_to_json(store_lists)


# def modify_by_name(name, modify_json):
#     """
#
#     :param name:
#     :type name:
#     :param modify_json:
#     :type modify_json:
#     :return: number of row update, 0 if not find, error if modify_json is wrong
#     :rtype: int
#     """
#     query = StoreList.update(**modify_json).where(StoreList.name == name)
#     return query.execute()
#
#
# def remove_by_name(name):
#     query = StoreList.delete().where(StoreList.name == name)
#     return query.execute()

