# encoding: utf-8
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
from server.service import e_bike_model_service
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
    storage = Storage.select()
    return models_to_json(storage)


def get_by_id(store_list_id):
    return model_to_dict(Storage.get(Storage.id == store_list_id))


def get_by_model_color(model, color):
    storage = Storage.select().where(
        Storage.model == model, color == color)
    return models_to_json(storage)


def get_storage(model):
    """通过车型获取 该车型所有库存分类

    :param model:
    :type model:
    :return: 该车型所有库存
    :rtype: json
    """
    storage = Storage.select().where(
        Storage.model == model)
    return models_to_json(storage)


def get_storage_total(model):
    """通过车型获取 该车型库存总数

    :param model:
    :type model:
    :return:
    :rtype:
    """
    storage = Storage.select().where(
        Storage.model == model)
    count = 0
    for one in storage:
        count += one.num
    return count


def modify_num(model, color, num):
    """

    :param model:
    :type model:
    :param color:
    :type color:
    :param num:
    :type num:
    :return: number of row update, 0 if not find, error if modify_json is wrong
    :rtype: int
    """
    query = Storage.update(num=num).where(
        Storage.model == model, Storage.color == color)
    return query.execute()


def decrement_num(model, color):
    query = Storage.update(num=Storage.num - 1) \
        .where(Storage.model == model, Storage.color == color)
    return query.execute()


def increment_num(model, color):
    query = Storage.update(num=Storage.num + 1) \
        .where(Storage.model == model, Storage.color == color)
    return query.execute()


def check_storage(model, color):
    storage = Storage.select().where(
        Storage.model == model, Storage.color == color).get()
    if storage and storage.num > 0:
        return True
    else:
        return False


# ***************************** test ***************************** #
# def decrement_test():  # complete
#     logger.debug(decrement_num(model="E100小龟",
#                                color="红"))
#
#
# def modify_num_test():  # complete
#     logger.debug(modify_num(model="E100小龟",
#                             color="红", num=10))


def add_template():
    template_json = [
        {
            "model": "E100小龟",
            "color": "蓝",
            "num": 50
        },
        {
            "model": "E100小龟",
            "color": "红",
            "num": 50
        },
        {
            "model": "E101小龟",
            "color": "红",
            "num": 50
        }
    ]
    for json in template_json:
        result = add(**json)
        logger.debug(result)


# 增加库存脚本 为每个电动车类型增加库存
def add_script():
    # 从 e_bike_model 提取
    e_bike_models = e_bike_model_service.get_all()
    for e_bike_model in e_bike_models:
        model = e_bike_model.name
        colors = e_bike_model.colors
        # colors = colors.split("、")
        num = 50
        for color in colors:
            result = add(model=model, color=color, num=num)
            if not result:
                logger.error("add error")


if __name__ == '__main__':

    add_script()

