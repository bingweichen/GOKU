"""

@author: Bingwei Chen

@time: 2017.08.08

@desc: service for store_list

1. 电动车销售库存 更改 Add/Get/Modify/Remove

1. 库存新增(完成）
2. 库存获取(完成）
3. 库存更改(完成）
4. 库存减一(完成）

"""
from playhouse.shortcuts import model_to_dict

from server.database.model import Storage
from server.utility.json_utility import models_to_json

from server.utility.logger import logger


def add(**kwargs):
    """
    add storage
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
    store_list = Storage.create(**kwargs)
    return model_to_dict(store_list)


def get(*query, **kwargs):
    store_list = Storage.get(*query, **kwargs)
    return model_to_dict(store_list)


def get_all():
    store_lists = Storage.select()
    return models_to_json(store_lists)


def get_by_id(store_list_id):
    return model_to_dict(Storage.get(Storage.id == store_list_id))


def get_by_model_color(model, color):
    store_lists = Storage.select().where(
        Storage.model == model, color == color)
    return models_to_json(store_lists)


def get_by_model(model):
    """通过车型获取 该车型所有库存

    :param model:
    :type model:
    :return: 该车型所有库存
    :rtype: json
    """
    store_lists = Storage.select().where(
        Storage.model == model)
    return models_to_json(store_lists)


def modify_num_by_id(storage_id, num):
    """

    :param storage_id:
    :type storage_id:
    :param num:
    :type num:
    :return: number of row update, 0 if not find, error if modify_json is wrong
    :rtype: int
    """
    query = Storage.update(num=num).where(Storage.id == storage_id)
    return query.execute()


def decrement_num(model, color):
    query = Storage.update(num=Storage.num - 1) \
        .where(Storage.model == model, color == color)
    logger.debug("increment".encode('utf-8'))
    return query.execute()


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
#     query = Storage.update(**modify_json).where(Storage.name == name)
#     return query.execute()
#
#
# def remove_by_name(name):
#     query = Storage.delete().where(Storage.name == name)
#     return query.execute()


# ***************************** test ***************************** #
def decrement_test():  # complete
    print(decrement_num(model="E100小龟",
                        color="红"))




# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        {
            "model": "E100小龟",
            "color": "红",
            "num": 50
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    pass
    print(get_all())
